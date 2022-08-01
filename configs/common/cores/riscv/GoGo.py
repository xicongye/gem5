from m5.objects import *

class GoGo_IntFU(MinorFU):
    opClasses = minorMakeOpClassSet(['IntAlu'])
    timings = [
      MinorFUTiming(
        suppress = False,
        extraCommitLat = 0,
        extraAssumedLat = 0,
        srcRegsRelativeLats = [],
        description = 'Int',
      )
    ]
    opLat = 1
    issueLat = 1
    cantForwardFromFUIndices = []


class GoGo_IntMulFU(MinorFU):
    opClasses = minorMakeOpClassSet(['IntMult'])
    timings = [
      MinorFUTiming(
        suppress = False,
        extraCommitLat = 0,
        extraAssumedLat = 0,
        srcRegsRelativeLats = [],
        description = 'Mul',
      )
    ]
    opLat = 2
    issueLat = 2


class GoGo_IntDivFU(MinorFU):
    opClasses = minorMakeOpClassSet(['IntDiv'])
    timings = [
      MinorFUTiming(
        suppress = False,
        extraCommitLat = 0,
        extraAssumedLat = 0,
        srcRegsRelativeLats = [],
        description = 'IntDiv',
        )
      ]
    opLat = 32
    issueLat = 32


class GoGo_MemFU(MinorFU):
    opClasses = minorMakeOpClassSet(['MemRead', 'MemWrite'])
    timings = [
      MinorFUTiming(
        suppress = False,
        extraCommitLat = 0,
        extraAssumedLat = 1,
        srcRegsRelativeLats = [],
        description='Mem',
        )
      ]
    opLat = 1
    issueLat = 1


### Dummy FU List Start ###

class GoGo_FloatSimdFU(MinorFU):
    opClasses = minorMakeOpClassSet([
        'FloatAdd', 'FloatCmp', 'FloatCvt', 'FloatMisc', 'FloatMult',
        'FloatMultAcc', 'FloatDiv', 'FloatSqrt',
        'SimdAdd', 'SimdAddAcc', 'SimdAlu', 'SimdCmp', 'SimdCvt',
        'SimdMisc', 'SimdMult', 'SimdMultAcc', 'SimdShift', 'SimdShiftAcc',
        'SimdDiv', 'SimdSqrt', 'SimdFloatAdd', 'SimdFloatAlu', 'SimdFloatCmp',
        'SimdFloatCvt', 'SimdFloatDiv', 'SimdFloatMisc', 'SimdFloatMult',
        'SimdFloatMultAcc', 'SimdFloatSqrt', 'SimdReduceAdd', 'SimdReduceAlu',
        'SimdReduceCmp', 'SimdFloatReduceAdd', 'SimdFloatReduceCmp',
        'SimdAes', 'SimdAesMix',
        'SimdSha1Hash', 'SimdSha1Hash2', 'SimdSha256Hash',
        'SimdSha256Hash2', 'SimdShaSigma2', 'SimdShaSigma3'])
    timings = [MinorFUTiming(description='FloatSimd',
        srcRegsRelativeLats=[2])]
    opLat = 6

class GoGo_PredFU(MinorFU):
    opClasses = minorMakeOpClassSet(['SimdPredAlu'])
    timings = [MinorFUTiming(description="Pred",
        srcRegsRelativeLats=[2])]
    opLat = 3

class GoGo_SimdMemFU(MinorFU):
    opClasses = minorMakeOpClassSet(['FloatMemRead',
                                     'FloatMemWrite'])
    timings = [MinorFUTiming(description='Mem',
        srcRegsRelativeLats=[1], extraAssumedLat=2)]
    opLat = 1

class GoGo_MiscFU(MinorFU):
    opClasses = minorMakeOpClassSet(['IprAccess', 'InstPrefetch'])
    opLat = 1

### Dummy FU List End ###



## FU Pool
class GoGo_FUPool(MinorFUPool):
    funcUnits = [GoGo_IntFU(), # 0
        GoGo_IntMulFU(), # 1
        GoGo_IntDivFU(), # 2
        GoGo_MemFU(), # 3
        GoGo_FloatSimdFU(), # 4
        GoGo_PredFU(), # 5
        GoGo_SimdMemFU(), # 6
        GoGo_MiscFU(), # 7
        ]


## Branch Predictor
class GoGo_BP(TournamentBP):
    localPredictorSize = 64
    localCtrBits = 2
    localHistoryTableSize = 64
    globalPredictorSize = 1024
    globalCtrBits = 2
    choicePredictorSize = 1024
    choiceCtrBits = 2
    BTBEntries = 2048
    BTBTagSize = 20
    RASSize = 8
    instShiftAmt = 1


## Cache
class GoGo_ICache(Cache):
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 1
    tgts_per_mshr = 1
    size = '32kB'
    assoc = 4
    is_read_only = True
    # Writeback clean lines as well
    writeback_clean = True


class GoGo_DCache(Cache):
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 1
    tgts_per_mshr = 1
    size = '32kB'
    assoc = 4
    write_buffers = 1
    # Consider the L2 a victim cache also for clean lines
    writeback_clean = True


class GoGo_MMU(RiscvMMU):
    itb = RiscvTLB(entry_type="instruction", size=32)
    dtb = RiscvTLB(entry_type="data", size=32)


class GoGo(MinorCPU):
    fetch1FetchLimit = 1
    fetch1LineSnapWidth = 0
    fetch1LineWidth = 0
    fetch1ToFetch2ForwardDelay = 1
    fetch1ToFetch2BackwardDelay = 1

    fetch2InputBufferSize = 5
    fetch2ToDecodeForwardDelay = 1
    fetch2CycleInput = True

    decodeInputBufferSize = 5
    decodeToExecuteForwardDelay = 1
    decodeInputWidth = 1
    decodeCycleInput = True

    executeInputWidth = 1
    executeCycleInput = True
    executeIssueLimit = 1

    executeMemoryIssueLimit = 1

    executeCommitLimit = 1
    executeMemoryCommitLimit = 1
    executeInputBufferSize = 5

    executeMaxAccessesInMemory = 1

    executeLSQMaxStoreBufferStoresPerCycle = 1
    executeLSQRequestsQueueSize = 1
    executeLSQTransfersQueueSize = 1
    executeLSQStoreBufferSize = 1
    executeBranchDelay = 1
    executeFuncUnits = GoGo_FUPool()
    executeSetTraceTimeOnCommit = True
    executeSetTraceTimeOnIssue = False

    executeAllowEarlyMemoryIssue = True
    enableIdling = True
    branchPred = GoGo_BP()
    mmu = GoGo_MMU()


# L2 Cache
class GoGo_L2(Cache):
    tag_latency = 12
    data_latency = 12
    response_latency = 12
    mshrs = 16
    tgts_per_mshr = 8
    size = '1MB'
    assoc = 16
    write_buffers = 8
    prefetch_on_access = True
    clusivity = 'mostly_excl'
    # Simple stride prefetcher
    prefetcher = StridePrefetcher(degree=8, latency = 1)
    tags = BaseSetAssoc()
    replacement_policy = RandomRP()

