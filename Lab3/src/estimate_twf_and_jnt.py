import argparse
import os
import sys

from sprocket.model.GMM import GMMConvertor, GMMTrainer
from sprocket.util import HDF5, estimate_twf, melcd
from sprocket.util import static_delta, align_data

from yml import SpeakerYML, PairYML
from misc import read_feats, extsddata, transform_jnt


def get_alignment(odata, onpow, tdata, tnpow, opow=-20, tpow=-20,
                  sd=0, cvdata=None, given_twf=None, otflag=None,
                  distance='melcd'):

    oexdata = extsddata(odata[:, sd:], onpow,
                        power_threshold=opow)
    texdata = extsddata(tdata[:, sd:], tnpow,
                        power_threshold=tpow)

    if cvdata is None:
        align_odata = oexdata
    else:
        cvexdata = extsddata(cvdata, onpow,
                             power_threshold=opow)
        align_odata = cvexdata

    if given_twf is None:
        twf = estimate_twf(align_odata, texdata,
                           distance=distance, otflag=otflag)
    else:
        twf = given_twf

    jdata = align_data(oexdata, texdata, twf)
    mcd = melcd(align_odata[twf[0]], texdata[twf[1]])

    return jdata, twf, mcd


def align_feature_vectors(odata, onpows, tdata, tnpows, pconf,
                          opow=-100, tpow=-100, itnum=3, sd=0,
                          given_twfs=None, otflag=None):

    num_files = len(odata)
    cvgmm, cvdata = None, None
    for it in range(1, itnum + 1):
        print('{}-th joint feature extraction starts.'.format(it))
        twfs, jfvs = [], []
        for i in range(num_files):
            if it == 1 and given_twfs is not None:
                gtwf = given_twfs[i]
            else:
                gtwf = None
            if it > 1:
                cvdata = cvgmm.convert(static_delta(odata[i][:, sd:]),
                                       cvtype=pconf.GMM_mcep_cvtype)
            jdata, twf, mcd = get_alignment(odata[i],
                                            onpows[i],
                                            tdata[i],
                                            tnpows[i],
                                            opow=opow,
                                            tpow=tpow,
                                            sd=sd,
                                            cvdata=cvdata,
                                            given_twf=gtwf,
                                            otflag=otflag)
            twfs.append(twf)
            jfvs.append(jdata)
            print('distortion [dB] for {}-th file: {}'.format(i + 1, mcd))
        jnt_data = transform_jnt(jfvs)

        if it != itnum:
            # train GMM, if not final iteration
            datagmm = GMMTrainer(n_mix=pconf.GMM_mcep_n_mix,
                                 n_iter=pconf.GMM_mcep_n_iter,
                                 covtype=pconf.GMM_mcep_covtype)
            datagmm.train(jnt_data)
            cvgmm = GMMConvertor(n_mix=pconf.GMM_mcep_n_mix,
                                 covtype=pconf.GMM_mcep_covtype)
            cvgmm.open_from_param(datagmm.param)
        it += 1
    return jfvs, twfs


def main(*argv):
    argv = argv if argv else sys.argv[1:]
    # Options for python
    description = 'estimate joint feature of source and target speakers'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('org_yml', type=str,
                        help='Yml file of the original speaker')
    parser.add_argument('tar_yml', type=str,
                        help='Yml file of the target speaker')
    parser.add_argument('pair_yml', type=str,
                        help='Yml file of the speaker pair')
    parser.add_argument('org_list_file', type=str,
                        help='List file of original speaker')
    parser.add_argument('tar_list_file', type=str,
                        help='List file of target speaker')
    parser.add_argument('pair_dir', type=str,
                        help='Directory path of h5 files')
    args = parser.parse_args(argv)

    # read speaker-dependent yml files
    oconf = SpeakerYML(args.org_yml)
    tconf = SpeakerYML(args.tar_yml)

    # read pair-dependent yml file
    pconf = PairYML(args.pair_yml)

    # read source and target features from HDF file
    h5_dir = os.path.join(args.pair_dir, 'h5')
    org_mceps = read_feats(args.org_list_file, h5_dir, ext='mcep')
    org_npows = read_feats(args.org_list_file, h5_dir, ext='npow')
    tar_mceps = read_feats(args.tar_list_file, h5_dir, ext='mcep')
    tar_npows = read_feats(args.tar_list_file, h5_dir, ext='npow')
    assert len(org_mceps) == len(tar_mceps)
    assert len(org_npows) == len(tar_npows)
    assert len(org_mceps) == len(org_npows)

    # dtw between original and target w/o 0th and silence
    print('## Alignment mcep w/o 0-th and silence ##')
    jmceps, twfs = align_feature_vectors(org_mceps,
                                         org_npows,
                                         tar_mceps,
                                         tar_npows,
                                         pconf,
                                         opow=oconf.power_threshold,
                                         tpow=tconf.power_threshold,
                                         itnum=pconf.jnt_n_iter,
                                         sd=1,
                                         )
    jnt_mcep = transform_jnt(jmceps)

    # create joint feature for codeap using given twfs
    print('## Alignment codeap using given twf ##')
    org_codeaps = read_feats(args.org_list_file, h5_dir, ext='codeap')
    tar_codeaps = read_feats(args.tar_list_file, h5_dir, ext='codeap')
    jcodeaps = []
    for i in range(len(org_codeaps)):
        # extract codeap joint feature vector
        jcodeap, _, _ = get_alignment(org_codeaps[i],
                                      org_npows[i],
                                      tar_codeaps[i],
                                      tar_npows[i],
                                      opow=oconf.power_threshold,
                                      tpow=tconf.power_threshold,
                                      given_twf=twfs[i])
        jcodeaps.append(jcodeap)
    jnt_codeap = transform_jnt(jcodeaps)

    # save joint feature vectors
    jnt_dir = os.path.join(args.pair_dir, 'jnt')
    os.makedirs(jnt_dir, exist_ok=True)
    jntpath = os.path.join(jnt_dir, 'it' + str(pconf.jnt_n_iter) + '_jnt.h5')
    jnth5 = HDF5(jntpath, mode='a')
    jnth5.save(jnt_mcep, ext='mcep')
    jnth5.save(jnt_codeap, ext='codeap')
    jnth5.close()

    # save twfs
    twf_dir = os.path.join(args.pair_dir, 'twf')
    os.makedirs(twf_dir, exist_ok=True)
    with open(args.org_list_file, 'r') as fp:
        for line, twf in zip(fp, twfs):
            f = os.path.basename(line.rstrip())
            twfpath = os.path.join(
                twf_dir, 'it' + str(pconf.jnt_n_iter) + '_' + f + '.h5')
            twfh5 = HDF5(twfpath, mode='a')
            twfh5.save(twf, ext='twf')
            twfh5.close()


if __name__ == '__main__':
    main()
