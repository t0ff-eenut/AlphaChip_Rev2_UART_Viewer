
import numpy as np
import time
import GUI
import copy

Q_ui32_uart_reg_revice_64bit = []
Q_ui32_CMD_32bit = []
A_REGISTERS = []

RW_2_NUM = {
    'NONE': 0,
    'R'   : 1,
    'W'   : 2,
    'RW'  : 3
    }

NUM_2_RW = {
    0 : 'NONE',
    1 : 'R',
    2 : 'W',
    3 : 'R/W'
    }

REG_INDEX = {
    'CPU_R/W'       : 0,
    'ISP_R/W'       : 1,
    'NAME'          : 2,
    'Default'       : 3,
    'Value'         : 3,
    'MIN'           : 4,
    'MAX'           : 5,
    'Bits'          : 6,
    'Start_Bits'    : 7
    }

REG_NAME_2_REG_NUM = {
    'CPU_SET_REGISTER'              : 0,
    'ISP_STS_REGISTER'              : 1,
    'ILL_STS_REGISTER'              : 2,
    'BIG_RESULT_STS_REGISTER'       : 3,
    'SMALL_RESULT_STS_REGISTER'     : 4,
    'SPI_SET_REGISTER'              : 5,
    'TP1_SET_REGISTER'              : 6,
    'WATCH_64_TP2_REGISTER'         : 7,
    'WATCH_16_TP2_REGISTER'         : 8,
    'ACTIVE_TP2_REGISTER'           : 9,
    'CIS_SET_REGISTER'              : 10,
    'ILL_SET_REGISTER'              : 11,
    'ADC_SET_REGISTER'              : 12,
    'COL_DATA_SET_REGISTER'         : 13,
    'LED_PWM_DIM_SET_REGISTER'      : 14,
    'LED_SEL_DIM_SET_REGISTER'      : 15,
    'PAD_OUT_SET_REGISTER'          : 16,
    'FRAME_SET_REGISTER'            : 17,
    'INT_TIME_MANUAL_SET_REGISTER'  : 18,
    'NONE'                          : 19,
    'PAD_CTRL'                      : 20,
    'CPU_DATA_0_REGISTER'           : 21,
    'CPU_DATA_1_REGISTER'           : 22, # NOW_CIS_SETTING_VALUE
    'CPU_DATA_2_REGISTER'           : 23, # NOW_CHIP_MODE_VALUE
    'CPU_DATA_3_REGISTER'           : 24, # CPU_ACTIVE_HIGHRECHECK_TP1
    'CPU_DATA_4_REGISTER'           : 25, # OCCU_TP2 # CPU_DETECT_TP1
    'CPU_DATA_5_REGISTER'           : 26, # LOW_RECHECK_MODE_TP2
    'CPU_DATA_6_REGISTER'           : 27, # ACTIVE_MODE_TP2
    'CPU_DATA_7_REGISTER'           : 28, # HIGH_RECHECK_MODE_TP2
    'CPU_DATA_8_REGISTER'           : 29, # DETECT_MODE_TP2
    'CPU_DATA_9_REGISTER'           : 30, # EXT_LIGHT_TH_SETTING
    'CPU_DATA_10_REGISTER'          : 31, # EXT_LIGHT_TP2_SETTING
    'CPU_DATA_11_REGISTER'          : 32, # TP_SETTING_INIT
    'CPU_DATA_12_REGISTER'          : 33, # INTTIME_SETTING_DATA
    'CPU_DATA_13_REGISTER'          : 34, # RECHECK_SETTING_DATA
    'CPU_DATA_14_REGISTER'          : 35, # TIMER_SETTING_DATA
    'CPU_DATA_15_REGISTER'          : 36, # PSEUDO_SETTING
    'CPU_DATA_16_REGISTER'          : 37, # CPU_MODE_CIS
    'CPU_DATA_17_REGISTER'          : 38, # INTERRUPT_NEW_FRAME
    'CPU_DATA_18_REGISTER'          : 39, # BACKUP_DATA # INTERRUPT_WATCH_CIS
    'CPU_DATA_19_REGISTER'          : 40, # RECHECK_ERROR_DATA
    'CPU_DATA_20_REGISTER'          : 41, # TP_BACKUP_DATA
    'CPU_DATA_21_REGISTER'          : 42, # CIS_ACTIVATION_SETTING_EN_DATA # CIS_ACTIVATION_SETTING_BINARY_INTTIME_POINTER_DATA # CIS_ACTIVATION_SETTING_TARGET_DATA
    'CPU_DATA_22_REGISTER'          : 43, # ALPHACHIP_CIS_SETTING_ERROR_DATA
    'CPU_DATA_23_REGISTER'          : 44, 
    'CPU_DATA_24_REGISTER'          : 45, 
    'CPU_DATA_25_REGISTER'          : 46, 
    'CPU_DATA_26_REGISTER'          : 47, 
    'CPU_DATA_27_REGISTER'          : 48, 
    'CPU_DATA_28_REGISTER'          : 49, 
    'CPU_DATA_29_REGISTER'          : 50, 
    'CPU_DATA_30_REGISTER'          : 51, 
    
    
    'NOW_CIS_SETTING_VALUE'         : 22,
    'NOW_CHIP_MODE_VALUE'           : 23,
    'CPU_ACTIVE_HIGHRECHECK_TP1'    : 24,
    'OCCU_TP2'                      : 25,
    'CPU_DETECT_TP1'                : 25,
    'LOW_RECHECK_MODE_TP2'          : 26,
    'ACTIVE_MODE_TP2'               : 27,
    'HIGH_RECHECK_MODE_TP2'         : 28,
    'DETECT_MODE_TP2'               : 29,
    'EXT_LIGHT_TH_SETTING'          : 30,
    'EXT_LIGHT_TP2_SETTING'         : 31,
    'TP_SETTING_INIT'               : 32,
    'INTTIME_SETTING_DATA'          : 33,
    'RECHECK_SETTING_DATA'          : 34,
    'TIMER_SETTING_DATA'            : 35,
    'PSEUDO_SETTING'                : 36,
    
    'CPU_MODE_CIS'                  : 37,
    'INTERRUPT_NEW_FRAME'           : 38,
    'BACKUP_DATA'                   : 39,
    'INTERRUPT_WATCH_CIS'           : 39,
    'RECHECK_ERROR_DATA'            : 40,
    'TP_BACKUP_DATA'                : 41,
    'CIS_ACTIVATION_SETTING_EN_DATA'                        : 42,
    'CIS_ACTIVATION_SETTING_BINARY_INTTIME_POINTER_DATA'    : 42,
    'CIS_ACTIVATION_SETTING_TARGET_DATA'                    : 42,
    'ALPHACHIP_CIS_SETTING_ERROR_DATA'                      : 43,
}

REG_NUM_2_REG_NAME = {
    0 : 'CPU_SET_REGISTER'            ,
    1 : 'ISP_STS_REGISTER'            ,
    2 : 'ILL_STS_REGISTER'            ,
    3 : 'BIG_RESULT_STS_REGISTER'     ,
    4 : 'SMALL_RESULT_STS_REGISTER'   ,
    5 : 'SPI_SET_REGISTER'            ,
    6 : 'TP1_SET_REGISTER'            ,
    7 : 'WATCH_64_TP2_REGISTER'       ,
    8 : 'WATCH_16_TP2_REGISTER'       ,
    9 : 'ACTIVE_TP2_REGISTER'         ,
    10 : 'CIS_SET_REGISTER'            ,
    11 : 'ILL_SET_REGISTER'            ,
    12 : 'ADC_SET_REGISTER'            ,
    13 : 'COL_DATA_SET_REGISTER'       ,
    14 : 'LED_PWM_DIM_SET_REGISTER'    ,
    15 : 'LED_SEL_DIM_SET_REGISTER'    ,
    16 : 'PAD_OUT_SET_REGISTER'        ,
    17 : 'FRAME_SET_REGISTER'          ,
    18 : 'INT_TIME_MANUAL_SET_REGISTER',
    19 : 'NONE'                        ,
    20 : 'PAD_CTRL'                    ,
    21 : 'CPU_DATA_0_REGISTER'         ,
    22 : 'CPU_DATA_1_REGISTER'         ,
    23 : 'CPU_DATA_2_REGISTER'         ,
    24 : 'CPU_DATA_3_REGISTER'         ,
    25 : 'CPU_DATA_4_REGISTER'         ,
    26 : 'CPU_DATA_5_REGISTER'         ,
    27 : 'CPU_DATA_6_REGISTER'         ,
    28 : 'CPU_DATA_7_REGISTER'         ,
    29 : 'CPU_DATA_8_REGISTER'         ,
    30 : 'CPU_DATA_9_REGISTER'         ,
    31 : 'CPU_DATA_10_REGISTER'        ,
    32 : 'CPU_DATA_11_REGISTER'        ,
    33 : 'CPU_DATA_12_REGISTER'        ,
    34 : 'CPU_DATA_13_REGISTER'        ,
    35 : 'CPU_DATA_14_REGISTER'        ,
    36 : 'CPU_DATA_15_REGISTER'        ,
    37 : 'CPU_DATA_16_REGISTER'        ,
    38 : 'CPU_DATA_17_REGISTER'        ,
    39 : 'CPU_DATA_18_REGISTER'        ,
    40 : 'CPU_DATA_19_REGISTER'        ,
    41 : 'CPU_DATA_20_REGISTER'        ,
    42 : 'CPU_DATA_21_REGISTER'        ,
    43 : 'CPU_DATA_22_REGISTER'        ,
    44 : 'CPU_DATA_23_REGISTER'        ,
    45 : 'CPU_DATA_24_REGISTER'        ,
    46 : 'CPU_DATA_25_REGISTER'        ,
    47 : 'CPU_DATA_26_REGISTER'        ,
    48 : 'CPU_DATA_27_REGISTER'        ,
    49 : 'CPU_DATA_28_REGISTER'        ,
    50 : 'CPU_DATA_29_REGISTER'        ,
    51 : 'CPU_DATA_30_REGISTER'        ,
}

TARGET = {
    'PIRA_1'    : 0,
    'PIRA_2'    : 1,
    'SSL_G_1'   : 2,
    'SSL_G_2'   : 3,
    'SSL_E'     : 4,
    'SPI'       : 5,
    'IO_TEST'   : 6
    }
CPU_WAKE_UP_CHECK = {
    '1ms' : 0,
    '2ms' : 1,
    '3ms' : 2,
    '4ms' : 3,
    '5ms' : 4,
    '6ms' : 5,
    '7ms' : 6,
    '8ms' : 7
    }

# 0
CPU_SET_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                     Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLK_F_PULSE_EN',         0,          0,      1,      1,      31],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLK_AHB_EN',             0,          0,      1,      1,      30],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLK_DATA_EN',            0,          0,      1,      1,      29],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLK_LED_EN',             0,          0,      1,      1,      28],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLK_CPU_EN',             0,          0,      1,      1,      27],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLK_REG_EN',             0,          0,      1,      1,      26],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLK_SPI_EN',             0,          0,      1,      1,      25],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLK_ADC_EN',             0,          0,      1,      1,      24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLEAR_BUFFER',           0,          0,      1,      1,      23],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'TARGET',                 0,          0,      5,      3,      20],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLEAR_INT_THERMAL_HIGH', 0,          0,      5,      3,      19],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLEAR_INT_EXT_BTN',      0,          0,      1,      1,      18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLEAR_INT_WATCH_SET',    0,          0,      1,      1,      17],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLEAR_INT_NEW_FRAME',    0,          0,      1,      1,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_MODE',               0,          0,      4,      3,      13],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_MODE_ENABLE',        0,          0,      1,      1,      12],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'DIFF_MODE_CNT_SET',      2,          1,      3,      2,      10],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_WAKE_UP_CHECK_TIME', 7,          0,      7,      3,      5],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_WAKE_UP_CHECK',      0,          0,      1,      1,      4],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_ALWAYS_ON',          0,          0,      1,      1,      3],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CLK_OUT_DISABLE',        0,          0,      1,      1,      2],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'INT_ENABLE',             0,          0,      1,      1,      1],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_DONE',               0,          0,      1,      1,      0]
    ]
A_REGISTERS.append(CPU_SET_REGISTER)

CHIP_MODE_STS = {
    'IDLE_MODE'     : 0,
    'POWER_ON_MODE' : 1,
    'STAND_BY_MODE' : 2,
    'WATCH_MODE'    : 3,
    'ACTIVE_MODE'   : 4
    }
WAKE_UP_STS = {
    'NONE'                      : 0, 
    'POWER_ON_SETTING'          : 1,
    'WATCH_SETTING'             : 2,
    'EXTERNAL_BTN_EN'           : 3,
    'ACTIVE_PIRA1'              : 4,
    'ACTIVE_PIRA2'              : 5,
    'ACTIVE_SSLG_DETECT'        : 6,
    'ACTIVE_SSLG_LOW_RECHECK'   : 7,
    'ACTIVE_SSLE'               : 8
    }
SCALE_STS = {
    '64x64' : 0,
    '16x16' : 1
    }
FRAME_BUF_STS = {
    'NONE' : 0,
    'READ' : 1,
    'WRITE' : 2,
    'READ_WRITE' : 3
    }
# 1
ISP_STS_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                   Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'CHIP_MODE_STS',        0,          0,      5,      3,      29],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'DAY_STS',              0,          0,      1,      1,      28],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'THERAML_STS',          0,          0,      1,      1,      27],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'INT_THERMAL_HIGH',     0,          0,      1,      1,      23],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'INT_EXT_BTN',          0,          0,      1,      1,      22],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'INT_WATCH_SET',        0,          0,      1,      1,      21],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'INT_NEW_FRAME',        0,          0,      1,      1,      20],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'WAKE_UP_STS',          0,          0,      8,      4,      16],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'LED_LEVEL_STS',        0,          0,      10,     4,      12],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'Pseudo_LED_STS',       0,          0,      1,      1,      11],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'CHIP_FRAME_SPEED_STS', 0,          0,      5,      3,      8],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'CHIP_SCALE_STS',       0,          0,      1,      1,      7],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'SIG_WAIT_STS',         0,          0,      1,      1,      6],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'DIMMING_DONE_STS',     0,          0,      1,      1,      5],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'FRAME_BUF_B_STS',      0,          0,      3,      2,      2],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'FRAME_BUF_A_STS',      0,          0,      3,      2,      0]
    ]
A_REGISTERS.append(ISP_STS_REGISTER)
    
# 2
ILL_STS_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                 Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'ILL_data_delta_old', 0,          0,      255,    8,      24],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'ILL_data_delta_now', 0,          0,      255,    8,      16],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'ILL_data_old',       0,          0,      255,    8,      8],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'ILL_data_now',       0,          0,      255,    8,      0]
    ]
A_REGISTERS.append(ILL_STS_REGISTER)
    
# 3
BIG_RESULT_STS_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                  Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'BIG_Result_data_buf', 0,          0,      32767,  16,     16],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'BIG_Result_data',     0,          0,      4096,   13,     0]
    ]
A_REGISTERS.append(BIG_RESULT_STS_REGISTER)

# 4
SMALL_RESULT_STS_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                    Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'SMALL_Result_data_buf', 0,          0,      32767,  16,     16],
    [RW_2_NUM['R'], RW_2_NUM['RW'], 'SMALL_Result_data',     0,          0,      4096,   13,     0]
    ]
A_REGISTERS.append(SMALL_RESULT_STS_REGISTER)

# 5
SPI_SET_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,             Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SPI_TIME_I',     49,         1,      255,    8,      8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SPI_TIME_L',     1,          1,      7,      3,      5],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SPI_TIME_T',     1,          1,      7,      3,      2],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SCK_OPT',        1,          0,      1,      1,      1],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SPI_OUT_EN',     0,          0,      1,      1,      0]
    ]
A_REGISTERS.append(SPI_SET_REGISTER)

# 6
TP1_SET_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                 Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_BIG_TP1',     15,         0,      255,    8,      24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_SMALL_TP1',   10,         0,      255,    8,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_BIG_TP1',      10,         0,      255,    8,      8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_SMALL_TP1',    5,          0,      255,    8,      0]
    ]
A_REGISTERS.append(TP1_SET_REGISTER)

# 7
WATCH_64_TP2_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                 Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_64_TP2_MAX',   4000,       0,      4096,   13,     16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_64_TP2_MIN',   150,        0,      4096,   13,     0]
    ]
A_REGISTERS.append(WATCH_64_TP2_REGISTER)

# 8
WATCH_16_TP2_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                 Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_16_TP2_MAX',   200,        0,      256,    9,      9],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_16_TP2_MIN',   20,         0,      256,    9,      0]
    ]
A_REGISTERS.append(WATCH_16_TP2_REGISTER)

# 9
ACTIVE_TP2_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                 Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_TP2_MAX',     4000,       0,      4096,    13,    16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_TP2_MIN',     150,        0,      4096,    13,    0]
    ]
A_REGISTERS.append(ACTIVE_TP2_REGISTER)

CIS_SET_MODE = {
    'WATCH'     : 2,
    'ACTIVE'    : 1,
    'RAW'       : 0
    }
CIS_SET_INDEX_GAIN      = 0
CIS_SET_INDEX_INTTIME   = 1
# 10
CIS_SET_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                    Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'RAW_INT_TIME_LEVEL',    18,         0,      31,     5,      18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'RAW_AMP_GAIN',          1,          0,      3,      2,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_INT_TIME_LEVEL', 18,         0,      31,     5,      18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_AMP_GAIN',       1,          0,      3,      2,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_INT_TIME_LEVEL',  18,         0,      31,     5,      18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_AMP_GAIN',        1,          0,      3,      2,      16]
    ]
A_REGISTERS.append(CIS_SET_REGISTER)

# 11
ILL_SET_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                 Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ILL_DARK_TP',        70,         0,      255,    8,      24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_ILL_Delta_TP', 30,         0,      255,    8,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ILL_RANGE_MAX',      127,        0,      255,    8,      8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ILL_RANGE_MIN',      64,         0,      255,    8,      0]
    ]
A_REGISTERS.append(ILL_SET_REGISTER)

ADC_SET_RESOL_MODE = {
    'ACTIVE'    : 0,
    'WATCH'     : 1,
    'RAW'       : 2
    }
ADC_SET_ADC_MODE = {
    'ACTIVE'    : 5,
    'WATCH'     : 6,
    'RAW'       : 7
    }
ADC_SET_OFFSET_INDEX = {
    'ENABLE'    : 10,
    'SIGN'      : 11,
    'OFFSET'    : 12
    }
# 12
ADC_SET_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                 Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_RESOL',       0,          0,      1,      1,      20],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_RESOL',        1,          0,      1,      1,      19],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'STANDBY_RESOL',      1,          0,      1,      1,      18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'POWER_ON_RESOL',     0,          0,      1,      1,      17],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'IDLE_RESOL',         0,          0,      1,      1,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_ADC_OPT',     1,          0,      1,      1,      15],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_ADC_OPT',      1,          0,      1,      1,      14],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'STANDBY_ADC_OPT',    1,          0,      1,      1,      13],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SEL_PN',             0,          0,      1,      1,      12],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SUM_OPT',            0,          0,      1,      1,      10],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'OFFSET_ENABLE',      0,          0,      1,      1,      9],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'OFFSET_SIGN',        0,          0,      1,      1,      8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'OFFSET_PIXEL_DATA',  0,          0,      255,    2,      0]
    ]
A_REGISTERS.append(ADC_SET_REGISTER)

# 13
COL_DATA_SET_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                         Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SUS_COMP_BIAS_MARGIN_SEL',   5,          1,      15,      4,      28],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SUS_CIS_BIAS_MARGIN_SEL',    5,          1,      15,      4,      24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SUS_AMP_MARGIN_SEL',         5,          0,      15,      4,      20],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SUS_AMP_OPT',                2,          0,      2,       2,      18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'DELAY_2us_STEP',             3,          0,      3,       2,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'HIGH_3us_STEP',              5,          0,      6,       3,      13],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SIDE_3us_STEP',              5,          0,      6,       3,      10],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'RESET_x_DATA_SET',           9,          0,      19,      5,      5],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'TX_DATA_SET',                9,          0,      19,      5,      0]
    ]
A_REGISTERS.append(COL_DATA_SET_REGISTER)


DIM_OPT = {
    '100Hz'     : 0,
    '200Hz'     : 1,
    'LED_Count' : 2,
    }

# 14
LED_PWM_DIM_SET_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                     Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'DIM_OPT',                0,          0,      2,      2,      29],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'PWM_DIM_TIMMING',        5,          0,      31,     5,      24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'RECHECK_PWM_DIM_LEV',    7,          0,      10,     4,      20],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'PWM_DIM_LEV4',           10,         0,      10,     4,      12],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'PWM_DIM_LEV3',           8,          0,      10,     4,      8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'PWM_DIM_LEV2',           6,          0,      10,     4,      4],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'PWM_DIM_LEV1',           4,          0,      10,     4,      0]
    ]
A_REGISTERS.append(LED_PWM_DIM_SET_REGISTER)

# 15
LED_SEL_DIM_SET_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                     Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'RECHECK_SEL_DIM_LEV',    1,          0,      4,      3,      12],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SEL_DIM_LEV4',           4,          0,      4,      3,      9],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SEL_DIM_LEV3',           3,          0,      4,      3,      6],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SEL_DIM_LEV2',           2,          0,      4,      3,      3],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SEL_DIM_LEV1',           1,          0,      4,      3,      0]
    ]
A_REGISTERS.append(LED_SEL_DIM_SET_REGISTER)

LED_BIAS = {        # 단위 us
    '0'     : 10,
    '1'     : 15,
    '2'     : 20,
    '3'     : 25,
    '4'     : 30,
    '5'     : 35,
    '6'     : 40,
    '7'     : 45,
    '8'     : 50,
    '9'     : 55,
    '10'    : 60,
    '11'    : 65,
    '12'    : 70,
    '13'    : 75,
    '14'    : 80,
    '15'    : 85,
    '16'    : 90,
    '17'    : 95,
    '18'    : 100,
    }
# 16
PAD_OUT_SET_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                         Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'DIM_ON_EN',                  0,          0,      1,      1,      31],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'DIM_OFF_EN',                 0,          0,      1,      1,      30],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'RECHK_ON_EN',                0,          0,      1,      1,      29],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'LED_ON_EN',                  0,          0,      1,      1,      28],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SUS_LED_BIAS_MARGIN_SEL',    5,          1,      4,      4,      24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'PIRA1_OUT_EN',               0,          0,      1,      1,      22],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'PIRA1_PULSE_OPT',            0,          0,      1,      1,      21],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'DIM_LED_SEQ_SET',            0,          0,      23,     5,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'LED_SEL',                    15,         1,      15,     4,      8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'PIRA_REG_B_SEL',             12,         1,      15,     4,      4],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'PIRA_REG_A_SEL',             3,          1,      15,     4,      0],
    ]
A_REGISTERS.append(PAD_OUT_SET_REGISTER)
    
FRAME_SPEED = {
    '1FRAME'    : 0,
    '2FRAME'    : 1,
    '3FRAME'    : 2,
    '4FRAME'    : 3,
    '6FRAME'    : 4,
    '12FRAME'   : 5
    }
FRAME_SET_MODE = {
    'WATCH'     : 7,
    'ACTIVE'    : 6,
    'RAW'       : 9
    }
# 17
FRAME_SET_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                     Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'STANDBY_FRAME_SEC_EN',   0,          0,      1,      1,      31],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'STANDBY_FRAME_SEC',      10,         1,      127,    7,      24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_FRAME_CNT_MAX',    5,          1,      15,     4,      20],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_FRAME_SEC',        5,          1,      15,     4,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_FRAME_SEC_EN',     0,          0,      1,      1,      15],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_FRAME',           5,          0,      5,      3,      12],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_FRAME',            2,          0,      5,      3,      9],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'STANDBY_FRAME',          0,          0,      5,      3,      6],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'POWER_ON_FRAME',         5,          0,      5,      3,      3],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'IDLE_FRAME',             5,          0,      5,      3,      0]
    ]
A_REGISTERS.append(FRAME_SET_REGISTER)

# 18
INT_TIME_MANUAL_SET_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                             Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_INT_MANUAL_SET_ENABLE',   0,          0,      1,      1,      31],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_INT_TIME_MANUAL_SET',     10000,      0,      20000,  15,     16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_INT_MANUAL_SET_ENABLE',    0,          0,      1,      1,      15],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'WATCH_INT_TIME_MANUAL_SET',      10000,      0,      20000,  15,     0]
    ]
A_REGISTERS.append(INT_TIME_MANUAL_SET_REGISTER)

# 19
NONE = [
#   CPU R/W,    ISP R/W,  NAME,                             Default,    MIN,    MAX,    Bits,    Start_Bits
    ]
A_REGISTERS.append(NONE)
    
# 20
PAD_CTRL = [
#   CPU R/W,    ISP R/W,  NAME,          Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[9]_1',   0,          0,      1,      1,      19],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[9]_0',   0,          0,      1,      1,      18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[8]_1',   0,          0,      1,      1,      17],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[8]_0',   0,          0,      1,      1,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[7]_1',   0,          0,      1,      1,      15],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[7]_0',   0,          0,      1,      1,      14],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[6]_1',   0,          0,      1,      1,      13],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[6]_0',   0,          0,      1,      1,      12],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[5]_1',   0,          0,      1,      1,      11],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[5]_0',   0,          0,      1,      1,      10],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[4]_1',   0,          0,      1,      1,      9],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[4]_0',   0,          0,      1,      1,      8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[3]_1',   0,          0,      1,      1,      7],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[3]_0',   0,          0,      1,      1,      6],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[2]_1',   0,          0,      1,      1,      5],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[2]_0',   0,          0,      1,      1,      4],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[1]_1',   0,          0,      1,      1,      3],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[1]_0',   0,          0,      1,      1,      2],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[0]_1',   0,          0,      1,      1,      1],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'GPIO[0]_0',   0,          0,      1,      1,      0]
    ]
A_REGISTERS.append(PAD_CTRL)

# 21
CPU_DATA_0_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,     Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['R'], RW_2_NUM['R'], 'C',       12,         12,     12,     4,      12],
    [RW_2_NUM['R'], RW_2_NUM['R'], 'C',       12,         12,     12,     4,      8],
    [RW_2_NUM['R'], RW_2_NUM['R'], 'D',       13,         13,     13,     4,      4],
    [RW_2_NUM['R'], RW_2_NUM['R'], 'D',       13,         13,     13,     4,      0]
    ]
A_REGISTERS.append(CPU_DATA_0_REGISTER)

# 22
CPU_DATA_1_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                                 Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_HIGH_RECHECK_CIS_SETTING_MAX',   0,          0,      1,      1,      25],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_HIGH_RECHECK_CIS_SETTING_MIN',   0,          0,      1,      1,      24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_ACTIVE_CIS_SETTING_MAX',         0,          0,      1,      1,      23],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_ACTIVE_CIS_SETTING_MIN',         0,          0,      1,      1,      22],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_DETECT_CIS_SETTING_MAX',         0,          0,      1,      1,      21],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_DETECT_CIS_SETTING_MIN',         0,          0,      1,      1,      20],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_LOW_RECHECK_CIS_SETTING_MAX',    0,          0,      1,      1,      19],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_LOW_RECHECK_CIS_SETTING_MIN',    0,          0,      1,      1,      18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_WATCH_CIS_SETTING_MAX',          0,          0,      1,      1,      17],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_WATCH_CIS_SETTING_MIN',          0,          0,      1,      1,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'NOW_CIS_MODE',                       0,          0,      7,      4,      7],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'NOW_INTTIME',                        0,          0,      31,     5,      2],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'NOW_GAIN',                           0,          0,      3,      2,      0],
    ]
A_REGISTERS.append(CPU_DATA_1_REGISTER)

SYS_STS = {
    'SYS_NONE'                          : 0, 
    'SYS_POWER_ON'                      : 1,
    'SYS_LOW_RECHECK'                   : 2,
    'SYS_LED_ON'                        : 3,
    'SYS_DETECT'                        : 4,
    'SYS_ACTIVE'                        : 5,
    'SYS_HIGH_RECHECK_LED_TIME_OUT'     : 6,
    'SYS_HIGH_RECHECK_MODE_TIME_OUT'    : 7,
    'SYS_WATCH_CIS_SETTING'             : 8,
    'SYS_ACTIVE_CIS_SETTING'            : 9
    }
# 23
CPU_DATA_2_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                                     Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_INTERRUPT_FUNCTION_EN',              0,          0,      1,      1,      31],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_CIS_SETTING_ACTIVATION_FUNCTION_EN', 0,          0,      1,      1,      30],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_TP_SETTING_EN',                      0,          0,      1,      1,      29],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_RECHECK_FUNCTION_EN',                0,          0,      1,      1,      28],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_INTTIME_SET_FUNCTION_EN',            0,          0,      1,      1,      27],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_GAIN_SET_FUNCTION_EN',               0,          0,      1,      1,      26],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_HIGH_RECHECK_MODE_EN',               0,          0,      1,      1,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_ACTIVE_MODE_EN',                     0,          0,      1,      1,      15],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_DETECT_MODE_EN',                     0,          0,      1,      1,      14],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_LED_ON_MODE_EN',                     0,          0,      1,      1,      13],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_LOW_RECHECK_MODE_EN',                0,          0,      1,      1,      12],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_POWER_ON_MODE_EN',                   0,          0,      1,      1,      11],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_ALPHACHIP_MODE_EN',                  0,          0,      1,      1,      10],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_MODE_START_EN',                      0,          0,      1,      1,      9],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_MAIN_EN',                            0,          0,      1,      1,      8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_NEW_FRAME_DONE',                     0,          0,      1,      1,      4],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_MODE_STS',                           0,          0,      9,      4,      0],
    ]
A_REGISTERS.append(CPU_DATA_2_REGISTER)

# 24
CPU_DATA_3_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                         Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'HIGH_RECHECK_BIG_TP1',       0,          0,      255,    8,      24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'HIGH_RECHECK_SMALL_TP1',     0,          0,      255,    8,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_MODE_BIG_TP1',        0,          0,      255,    8,      8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_MODE_SMALL_TP1',      0,          0,      255,    8,      0],
    ]
A_REGISTERS.append(CPU_DATA_3_REGISTER)

# 25
CPU_DATA_4_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                         Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'BIG_TP2_MIN',                0,          0,      4096,   13,     16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'DETECT_MODE_BIG_TP1',        0,          0,      255,    8,      8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'DETECT_MODE_SMALL_TP1',      0,          0,      255,    8,      0],
    ]
A_REGISTERS.append(CPU_DATA_4_REGISTER)

# 26
CPU_DATA_5_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                     Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'LOW_RECHECK_TP2_MAX',    0,          0,      4096,   13,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'LOW_RECHECK_TP2_MIN',    0,          0,      4096,   13,      0],
    ]
A_REGISTERS.append(CPU_DATA_5_REGISTER)

# 27
CPU_DATA_6_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_TP2_MAX',    0,          0,      4096,   13,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_TP2_MIN',    0,          0,      4096,   13,      0],
    ]
A_REGISTERS.append(CPU_DATA_6_REGISTER)

# 28
CPU_DATA_7_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                      Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'HIGH_RECHECK_TP2_MAX',    0,          0,      4096,   13,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'HIGH_RECHECK_TP2_MIN',    0,          0,      4096,   13,      0],
    ]
A_REGISTERS.append(CPU_DATA_7_REGISTER)

# 29
CPU_DATA_8_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'DETECT_TP2_MAX',    0,          0,      4096,   13,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'DETECT_TP2_MIN',    0,          0,      4096,   13,      0],
    ]
A_REGISTERS.append(CPU_DATA_8_REGISTER)

# 30
CPU_DATA_9_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                                         Default,    MIN,    MAX,   Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'FRAME_ILL_DELTA_TH_MARGIN',                  0,          0,      255,   8,       24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'LIGHT_ON_OFF_ILL_DELTA_TH_SETTING_MARGIN',   0,          0,      255,   8,       16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'TP2_MAX_MARGIN',                             0,          0,      255,   8,       8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'EXT_LED_ILL_DELTA_TP',                       0,          0,      255,   8,       0],
    ]
A_REGISTERS.append(CPU_DATA_9_REGISTER)

# 31
CPU_DATA_10_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                             Default,    MIN,    MAX,   Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'EXT_LED_ILL_DELTA_TP_MARGIN',    0,          0,      4096,  13,      16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SMALL_TP2_RESUALT_OLD',          0,          0,      4096,  13,      0],
    ]
A_REGISTERS.append(CPU_DATA_10_REGISTER)

# 32
CPU_DATA_11_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                                 Default,    MIN,    MAX,   Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'TP_SETTING_STABLE_RESUALT_COUNT',    0,          0,      31,    5,       27],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'TP_SETTING_TP2_LIMIT_16',            0,          0,      256,   9,       16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'TP_SETTING_TP2_LIMIT_64',            0,          0,      4096,  13,      0],
    ]
A_REGISTERS.append(CPU_DATA_11_REGISTER)

# 33
CPU_DATA_12_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,             Default,    MIN,    MAX,   Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_INT_MAX',    0,          0,      31,    5,       24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_INT_MIN',    0,          0,      31,    5,       6],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_INT_MAX',    0,          0,      31,    5,       8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_INT_MIN',    0,          0,      31,    5,       0],
    ]
A_REGISTERS.append(CPU_DATA_12_REGISTER)

# 34
CPU_DATA_13_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                     Default,    MIN,    MAX,   Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'RECHECK_COUNT',          0,          0,      15,    4,       16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'BYPASS_OPT',             0,          0,      1,     1,       15],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'NOT_CONT_OCCU_COUNT',    0,          0,      31,    5,       10],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CONT_OCCU_COUNT',        0,          0,      31,    5,       5],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'KNOW_OCCU_COUNT',        0,          0,      31,    5,       0],
    ]
A_REGISTERS.append(CPU_DATA_13_REGISTER)

# 35
CPU_DATA_14_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                     Default,    MIN,    MAX,   Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'HIGH_RECHECK_TIME',      0,          0,      255,   8,       24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'DETECT_MODE_TIMEOUT',    0,          0,      255,   8,       16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_MODE_TIMEOUT',    0,          0,      255,   8,       8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'LED_TIME_OUT',           0,          0,      255,   8,       5],
    ]
A_REGISTERS.append(CPU_DATA_14_REGISTER)

# 36
CPU_DATA_15_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                     Default,    MIN,    MAX,   Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'PSEUDO_SIGNAL_CYCLE',    0,          0,      255,   8,       0],
    ]
A_REGISTERS.append(CPU_DATA_15_REGISTER)

# 37
CPU_DATA_16_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                         Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_DETECT_INTTIME',         0,          0,      31,     5,       18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_DETECT_GAIN',            0,          0,      3,      2,       16],
    #[RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_DETECT_CIS',             0,          0,      3,      2,       0],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_HIGH_RECHECK_INTTIME',   0,          0,      31,     5,       10],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_HIGH_RECHECK_GAIN',      0,          0,      3,      2,       8],
    #[RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_HIGH_RECHECK_CIS',       0,          0,      3,      2,       0],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_ACTIVE_INTTIME',         0,          0,      31,     5,       2],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_ACTIVE_GAIN',            0,          0,      3,      2,       0],
    #[RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_ACTIVE_CIS',             0,          0,      3,      2,       0],
    ]
A_REGISTERS.append(CPU_DATA_16_REGISTER)

# 38
CPU_DATA_17_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                             Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_OCCU_BUFF_NOW',              0,          0,      1,      1,       16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_OCCU_BUFF',                  0,          0,      1,      1,       15],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'HIGH_CIS_RECHECK_ERROR_EN',      0,          0,      1,      1,       14],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'LOW_CIS_RECHECK_ERROR_EN',       0,          0,      1,      1,       13],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ILLU_IS_RANGE_OVER_ERROR_EN',    0,          0,      1,      1,       12],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ILLU_IS_RANGE_UNDER_ERROR_EN',   0,          0,      1,      1,       11],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'EXT_LED_TURN_ON_EN',             0,          0,      1,      1,       10],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'EXT_LED_TURN_OFF_EN',            0,          0,      1,      1,       9],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'EXT_LED_TH_EN',                  0,          0,      1,      1,       8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'EXT_LED_ILL_DELTA_EN',           0,          0,      1,      1,       7],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ILL_DELTA_SIGNAL_NOW',           0,          0,      1,      1,       6],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ILL_DELTA_SIGNAL_OLD',           0,          0,      1,      1,       5],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'OCCU_EN',                        0,          0,      1,      1,       4],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'BUFFER_KNOW_OCCU_EN',            0,          0,      1,      1,       3],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'BUFFER_CON_OCCU_EN',             0,          0,      1,      1,       2],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'BUFFER_CON_NOT_OCCU_EN',         0,          0,      1,      1,       1],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'BUFFER_NOW_OCCU_EN',             0,          0,      1,      1,       0],
    ]
A_REGISTERS.append(CPU_DATA_17_REGISTER)

# 39
CPU_DATA_18_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                                             Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_MODE_BACKUP_DONE',                           0,          0,      1,      1,       31],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'FRAME_SET_BACKUP',                               0,          0,      4096,   13,      27],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_MODE_BACKUP',                                0,          0,      7,      3,       24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'EXT_LED_ILL_DELTA_TP_BACKUP',                    0,          0,      255,    8,       16],

#   CPU R/W,    ISP R/W,  NAME,                                             Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_CIS_SETTING_NEED_NEW_FRAME_EN',           0,          0,      1,      1,       6],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVE_CIS_SETTING_EN',                          0,          0,      1,      1,       5],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'INTERRUPT_WATCH_CIS_SETTING_NEED_NEW_FRAME_EN',  0,          0,      1,      1,       4],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'INTERRUPT_WATCH_CIS_SETTING_LEVEL',              0,          0,      7,      3,       1],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'INTERRUPT_WATCH_CIS_SETTING_EN',                 0,          0,      1,      1,       0],
    ]
A_REGISTERS.append(CPU_DATA_18_REGISTER)

# 40
CPU_DATA_19_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                         Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'HIGH_RECHECK_ERROR_LIMIT',   0,          0,      15,     4,       28],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'HIGH_RECHECK_ERROR_COUNT',   0,          0,      15,     4,       24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'LOW_RECHECK_ERROR_LIMIT',    0,          0,      15,     4,       20],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'LOW_RECHECK_ERROR_COUNT',    0,          0,      15,     4,       16],
    
#   CPU R/W,    ISP R/W,  NAME,                         Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'CPU_CIS_SETTING_CHANGE_EN',  0,          0,      1,      1,       1],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_CIS_SETTING_CHANGE_EN',  0,          0,      1,      1,       0],
    ]
A_REGISTERS.append(CPU_DATA_19_REGISTER)

# 41
CPU_DATA_20_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                 Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'TP2_BACKUP',         0,          0,      4096,   13,       16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'TP1_BIG_BACKUP',     0,          0,      255,    8,        8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'TP1_SMALL_BACKUP',   0,          0,      255,    8,        0],
    #[RW_2_NUM['RW'], RW_2_NUM['R'], 'TP1_BACKUP',         0,          0,      15,     4,       16],
    ]
A_REGISTERS.append(CPU_DATA_20_REGISTER)

# 42
CPU_DATA_21_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                                                 Default,    MIN,    MAX,    Bits,    Start_Bits
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVATION_ILLU_TARGET_ILLU_IS_OVER_OF_TARGET_EN',   0,          0,      31,     5,       18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVATION_ILLU_TARGET_ILLU_IS_UNDER_OF_TARGET_EN',  0,          0,      31,     5,       18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVATION_ILLU_TARGET_FIND_INTTIME_EN',             0,          0,      31,     5,       18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ACTIVATION_ILLU_TARGET_ILLU_SAME_EN',                0,          0,      31,     5,       13],
    
#   CPU R/W,    ISP R/W,  NAME,                                                 Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'BINARY_MAX_POINTER',                                 0,          0,      31,     5,       18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'BINARY_MIN_POINTER',                                 0,          0,      31,     5,       13],
    
#   CPU R/W,    ISP R/W,  NAME,                                                 Default,    MIN,    MAX,    Bits,    Start_Bits    
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'TARGET_INTTIME',                                     0,          0,      31,     5,       8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'TARGET_ILLU',                                        0,          0,      255,    8,       0],
    ]
A_REGISTERS.append(CPU_DATA_21_REGISTER)

# 43
CPU_DATA_22_REGISTER = [
#   CPU R/W,    ISP R/W,  NAME,                             Default,    MIN,    MAX,    Bits,    Start_Bits 
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_HIGH_RECHECK_INTTIME_MAX',   0,          0,      1,      1,       27],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_HIGH_RECHECK_INTTIME_MIN',   0,          0,      1,      1,       26],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_ACTIVE_INTTIME_MAX',         0,          0,      1,      1,       25],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_ACTIVE_INTTIME_MIN',         0,          0,      1,      1,       24],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_DETECT_INTTIME_MAX',         0,          0,      1,      1,       23],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_DETECT_INTTIME_MIN',         0,          0,      1,      1,       22],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_LOW_RECHECK_INTTIME_MAX',    0,          0,      1,      1,       21],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_LOW_RECHECK_INTTIME_MIN',    0,          0,      1,      1,       20],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_WATCH_INTTIME_MAX',          0,          0,      1,      1,       19],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_WATCH_INTTIME_MIN',          0,          0,      1,      1,       18],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_RAW_INTTIME_MAX',            0,          0,      1,      1,       17],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_RAW_INTTIME_MIN',            0,          0,      1,      1,       16],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_HIGH_RECHECK_GAIN_MAX',      0,          0,      1,      1,       11],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_HIGH_RECHECK_GAIN_MIN',      0,          0,      1,      1,       10],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_ACTIVE_GAIN_MAX',            0,          0,      1,      1,       9],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_ACTIVE_GAIN_MIN',            0,          0,      1,      1,       8],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_DETECT_GAIN_MAX',            0,          0,      1,      1,       7],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_DETECT_GAIN_MIN',            0,          0,      1,      1,       6],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_LOW_RECHECK_GAIN_MAX',       0,          0,      1,      1,       5],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'SYS_LOW_RECHECK_GAIN_MIN',       0,          0,      1,      1,       4],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_WATCH_GAIN_MAX',             0,          0,      1,      1,       3],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_WATCH_GAIN_MIN',             0,          0,      1,      1,       2],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_RAW_GAIN_MAX',               0,          0,      1,      1,       1],
    [RW_2_NUM['RW'], RW_2_NUM['R'], 'ISP_RAW_GAIN_MIN',               0,          0,      1,      1,       0],
    ]
A_REGISTERS.append(CPU_DATA_22_REGISTER)

VALUE_INT = 0
VALUE_HEX = 1
VALUE_BIN = 2

def gen_32bit_process(A_register):
    i32_value_name_reg = 0
    for i_index_pointer in range(0, len(A_register), 1):
        i32_value_name_reg = i32_value_name_reg | (A_register[i_index_pointer][REG_INDEX['Value']] << A_register[i_index_pointer][REG_INDEX['Start_Bits']])
    return (i32_value_name_reg, hex(i32_value_name_reg), bin(i32_value_name_reg))


labelframe_reg_value_INDEX = {
                                'labelframe'    : 0,
                                'Number'        : 1,
                                'Addr'          : 2,
                                'CPU_R/W'       : 3,
                                'ISP_R/W'       : 4,
                                'Name'          : 5,
                                'Value'         : 6,
                                'Min'           : 7,
                                'Max'           : 8,
                                'Bits'          : 9,
                                'Start_Bit'     : 10
                                }

def reg_setting_process(i_addr, i_data):
    # i_reg_num = int((i_addr - 0x3D0000) / 8)
    i_reg_num = (i_addr - 0x3D0000) // 8
    i_reg_index_len = len(A_REGISTERS[i_reg_num])
    for i_index_sel in range(i_reg_index_len - 1, -1, -1):
        
# REG_INDEX = {
#     'CPU_R/W'       : 0,
#     'ISP_R/W'       : 1,
#     'NAME'          : 2,
#     'Default'       : 3,
#     'Value'         : 3,
#     'MIN'           : 4,
#     'MAX'           : 5,
#     'Bits'          : 6,
#     'Start_Bits'    : 7
#     }
        
        i_start_bits = A_REGISTERS[i_reg_num][i_index_sel][REG_INDEX['Start_Bits']]
        i_bits = A_REGISTERS[i_reg_num][i_index_sel][REG_INDEX['Bits']]
        
        # Mask 제작
        i_bit_mask = 0
        for i_bit in range(i_bits):
            i_bit_mask = i_bit_mask | (1 << i_bit)

        # 
        if A_REGISTERS[i_reg_num][i_index_sel][REG_INDEX['Value']] != (i_data & (i_bit_mask << i_start_bits)) >> i_start_bits:
            A_REGISTERS[i_reg_num][i_index_sel][REG_INDEX['Value']] = (i_data & (i_bit_mask << i_start_bits)) >> i_start_bits
            
            GUI.A_labelframe_reg_index[i_reg_num][i_index_sel][labelframe_reg_value_INDEX['Value']].configure( # :>08X
                text=f"{A_REGISTERS[i_reg_num][i_index_sel][REG_INDEX['Value']]:08X}"
            )

            s_reg_name = REG_NUM_2_REG_NAME[i_reg_num]
            reg_val_int = gen_32bit_process(A_REGISTERS[i_reg_num])[VALUE_INT]

            GUI.A_labelframe_reg_name[i_reg_num].configure( # :>08X
                text=GUI.reg_name_output(i_reg_num, s_reg_name, reg_val_int)
            )
    