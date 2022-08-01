from m5.objects import *

## FU List
class AutoMan_IntFU(MinorFU):
    opClasses = minorMakeOpClassSet(['IntAlu'])
    timings = [MinorFUTiming(description = 'Int',
       srcRegsRelativeLats = [])]
    opLat = 1

class AutoMan_IntMulFU(MinorFU):
    opClasses = minorMakeOpClassSet(['IntMult'])
    timings = [MinorFUTiming(description = 'Mul',
       srcRegsRelativeLats = [])]
    opLat = 2

class AutoMan_IntDivFU(MinorFU):
    opClasses = minorMakeOpClassSet(['IntDiv'])
    timings = [MinorFUTiming(description = 'IntDiv',
       srcRegsRelativeLats = [])]
    opLat = 18
    issueLat = 18

class AutoMan_MemFU(MinorFU):
    opClasses = minorMakeOpClassSet(['MemRead', 'MemWrite'])
    timings = [MinorFUTiming(description='Mem',
        srcRegsRelativeLats=[], extraAssumedLat=1)]
    opLat = 1


## FU Pool
class AutoMan_FUPool(MinorFUPool):
    funcUnits = [AutoMan_IntFU(), # 0
        AutoMan_IntMulFU(), # 1
        AutoMan_IntDivFU(), # 2
        AutoMan_MemFU() # 3
        ]

## Branch Predictor
class AutoMan_BP(TournamentBP):
    localPredictorSize = 64
    localCtrBits = 2
    localHistoryTableSize = 64
    globalPredictorSize = 1024
    globalCtrBits = 2
    choicePredictorSize = 1024
    choiceCtrBits = 2
    BTBEntries = 128
    BTBTagSize = 18
    RASSize = 8
    instShiftAmt = 2


## Cache
class AutoMan_ICache(Cache):
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


class AutoMan_DCache(Cache):
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


class AutoMan_MMU(RiscvMMU):
    itb = RiscvTLB(entry_type="instruction", size=32)
    dtb = RiscvTLB(entry_type="data", size=32)


class AutoMan(MinorCPU):
    fetch1FetchLimit = 1
    fetch1LineSnapWidth = 4
    fetch1LineWidth = 4
    fetch1ToFetch2ForwardDelay = 1
    fetch1ToFetch2BackwardDelay = 1

    fetch2InputBufferSize = 2
    fetch2ToDecodeForwardDelay = 1
    fetch2CycleInput = True

    decodeInputBufferSize = 2
    decodeToExecuteForwardDelay = 1
    decodeInputWidth = 1
    decodeCycleInput = True

    executeInputWidth = 2
    executeCycleInput = True
    executeIssueLimit = 1

    executeMemoryIssueLimit = 1

    executeCommitLimit = 1
    executeMemoryCommitLimit = 1
    executeInputBufferSize = 1

    executeMaxAccessesInMemory = 1

    executeLSQMaxStoreBufferStoresPerCycle = 1
    executeLSQRequestsQueueSize = 1
    executeLSQTransfersQueueSize = 1
    executeLSQStoreBufferSize = 1
    executeBranchDelay = 1
    executeFuncUnits = AutoMan_FUPool()
    executeSetTraceTimeOnCommit = True
    executeSetTraceTimeOnIssue = False

    executeAllowEarlyMemoryIssue = False
    enableIdling = True
    branchPred = AutoMan_BP()
    mmu = AutoMan_MMU()


# L2 Cache
class AutoMan_L2(Cache):
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

