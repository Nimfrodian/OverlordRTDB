#include"rtdb.h"


tS16S rtdb_assign_tS16S( tS16S* VarAddrs,
                       tU32 Indx,
                       tU8 Unit,
                       tS16 Min,
                       tS16 Def,
                       tS16 Max,
                       char* Comment )
{
    rtdb_arr_tS16S[Indx] = VarAddrs; // Copy address of variable to lookup table
    VarAddrs->tS16_val = Def;
    VarAddrs->tS16_min = Min;
    VarAddrs->tS16_def = Def;
    VarAddrs->tS16_max = Max;
    VarAddrs->ss.signalUnit = Unit;
    VarAddrs->ss.signalCmnt = Comment;
    VarAddrs->ss.signalState = SIGNAL_OK;
    VarAddrs->ss.objectStatus = OBJECT_STANDARD;
    VarAddrs->ss.crc32 = rtdb_calcCrc32(VarAddrs, sizeof(tS16S));
};

tS32S rtdb_assign_tS32S( tS32S* VarAddrs,
                       tU32 Indx,
                       tU8 Unit,
                       tS32 Min,
                       tS32 Def,
                       tS32 Max,
                       char* Comment )
{
    rtdb_arr_tS32S[Indx] = VarAddrs; // Copy address of variable to lookup table
    VarAddrs->tS32_val = Def;
    VarAddrs->tS32_min = Min;
    VarAddrs->tS32_def = Def;
    VarAddrs->tS32_max = Max;
    VarAddrs->ss.signalUnit = Unit;
    VarAddrs->ss.signalCmnt = Comment;
    VarAddrs->ss.signalState = SIGNAL_OK;
    VarAddrs->ss.objectStatus = OBJECT_STANDARD;
    VarAddrs->ss.crc32 = rtdb_calcCrc32(VarAddrs, sizeof(tS32S));
};

tU8S rtdb_assign_tU8S( tU8S* VarAddrs,
                       tU32 Indx,
                       tU8 Unit,
                       tU8 Min,
                       tU8 Def,
                       tU8 Max,
                       char* Comment )
{
    rtdb_arr_tU8S[Indx] = VarAddrs; // Copy address of variable to lookup table
    VarAddrs->tU8_val = Def;
    VarAddrs->tU8_min = Min;
    VarAddrs->tU8_def = Def;
    VarAddrs->tU8_max = Max;
    VarAddrs->ss.signalUnit = Unit;
    VarAddrs->ss.signalCmnt = Comment;
    VarAddrs->ss.signalState = SIGNAL_OK;
    VarAddrs->ss.objectStatus = OBJECT_STANDARD;
    VarAddrs->ss.crc32 = rtdb_calcCrc32(VarAddrs, sizeof(tU8S));
};

tU32S rtdb_assign_tU32S( tU32S* VarAddrs,
                       tU32 Indx,
                       tU8 Unit,
                       tU32 Min,
                       tU32 Def,
                       tU32 Max,
                       char* Comment )
{
    rtdb_arr_tU32S[Indx] = VarAddrs; // Copy address of variable to lookup table
    VarAddrs->tU32_val = Def;
    VarAddrs->tU32_min = Min;
    VarAddrs->tU32_def = Def;
    VarAddrs->tU32_max = Max;
    VarAddrs->ss.signalUnit = Unit;
    VarAddrs->ss.signalCmnt = Comment;
    VarAddrs->ss.signalState = SIGNAL_OK;
    VarAddrs->ss.objectStatus = OBJECT_STANDARD;
    VarAddrs->ss.crc32 = rtdb_calcCrc32(VarAddrs, sizeof(tU32S));
};

tF32S rtdb_assign_tF32S( tF32S* VarAddrs,
                       tU32 Indx,
                       tU8 Unit,
                       tF32 Min,
                       tF32 Def,
                       tF32 Max,
                       char* Comment )
{
    rtdb_arr_tF32S[Indx] = VarAddrs; // Copy address of variable to lookup table
    VarAddrs->tF32_val = Def;
    VarAddrs->tF32_min = Min;
    VarAddrs->tF32_def = Def;
    VarAddrs->tF32_max = Max;
    VarAddrs->ss.signalUnit = Unit;
    VarAddrs->ss.signalCmnt = Comment;
    VarAddrs->ss.signalState = SIGNAL_OK;
    VarAddrs->ss.objectStatus = OBJECT_STANDARD;
    VarAddrs->ss.crc32 = rtdb_calcCrc32(VarAddrs, sizeof(tF32S));
};

tES rtdb_assign_tES( tES* VarAddrs,
                       tU32 Indx,
                       tU8 Unit,
                       tE Min,
                       tE Def,
                       tE Max,
                       char* Comment )
{
    rtdb_arr_tES[Indx] = VarAddrs; // Copy address of variable to lookup table
    VarAddrs->tE_val = Def;
    VarAddrs->tE_min = Min;
    VarAddrs->tE_def = Def;
    VarAddrs->tE_max = Max;
    VarAddrs->ss.signalUnit = Unit;
    VarAddrs->ss.signalCmnt = Comment;
    VarAddrs->ss.signalState = SIGNAL_OK;
    VarAddrs->ss.objectStatus = OBJECT_STANDARD;
    VarAddrs->ss.crc32 = rtdb_calcCrc32(VarAddrs, sizeof(tES));
};

tU32 rtdb_write_tS16S( tS16S* VarAddrs, tS16 NewVal )
{
    tU32 stsCode = 0;
    tS16 valToWrite = VarAddrs->tS16_def;
    // check CRC
    if (rtdb_checkCrc32(VarAddrs, sizeof(VarAddrs)))
    {
        // TODO
    }
    // check for MIN
    else if ( NewVal < VarAddrs->tS16_min)
    {
        // TODO: Report error
        stsCode = 2;
    }
    // check for MAX
    else if ( NewVal > VarAddrs->tS16_max)
    {
        // TODO: Report error
        stsCode = 3;
    }
    else
    {
        if (OBJECT_STANDARD == VarAddrs->ss.objectStatus)
        {
            VarAddrs->tS16_val = NewVal;
            rtdb_calcCrc32( VarAddrs, sizeof(tS16S));
        }
    }

    return stsCode;
}

tU32 rtdb_write_tS32S( tS32S* VarAddrs, tS32 NewVal )
{
    tU32 stsCode = 0;
    tS32 valToWrite = VarAddrs->tS32_def;
    // check CRC
    if (rtdb_checkCrc32(VarAddrs, sizeof(VarAddrs)))
    {
        // TODO
    }
    // check for MIN
    else if ( NewVal < VarAddrs->tS32_min)
    {
        // TODO: Report error
        stsCode = 2;
    }
    // check for MAX
    else if ( NewVal > VarAddrs->tS32_max)
    {
        // TODO: Report error
        stsCode = 3;
    }
    else
    {
        if (OBJECT_STANDARD == VarAddrs->ss.objectStatus)
        {
            VarAddrs->tS32_val = NewVal;
            rtdb_calcCrc32( VarAddrs, sizeof(tS32S));
        }
    }

    return stsCode;
}

tU32 rtdb_write_tU8S( tU8S* VarAddrs, tU8 NewVal )
{
    tU32 stsCode = 0;
    tU8 valToWrite = VarAddrs->tU8_def;
    // check CRC
    if (rtdb_checkCrc32(VarAddrs, sizeof(VarAddrs)))
    {
        // TODO
    }
    // check for MIN
    else if ( NewVal < VarAddrs->tU8_min)
    {
        // TODO: Report error
        stsCode = 2;
    }
    // check for MAX
    else if ( NewVal > VarAddrs->tU8_max)
    {
        // TODO: Report error
        stsCode = 3;
    }
    else
    {
        if (OBJECT_STANDARD == VarAddrs->ss.objectStatus)
        {
            VarAddrs->tU8_val = NewVal;
            rtdb_calcCrc32( VarAddrs, sizeof(tU8S));
        }
    }

    return stsCode;
}

tU32 rtdb_write_tU32S( tU32S* VarAddrs, tU32 NewVal )
{
    tU32 stsCode = 0;
    tU32 valToWrite = VarAddrs->tU32_def;
    // check CRC
    if (rtdb_checkCrc32(VarAddrs, sizeof(VarAddrs)))
    {
        // TODO
    }
    // check for MIN
    else if ( NewVal < VarAddrs->tU32_min)
    {
        // TODO: Report error
        stsCode = 2;
    }
    // check for MAX
    else if ( NewVal > VarAddrs->tU32_max)
    {
        // TODO: Report error
        stsCode = 3;
    }
    else
    {
        if (OBJECT_STANDARD == VarAddrs->ss.objectStatus)
        {
            VarAddrs->tU32_val = NewVal;
            rtdb_calcCrc32( VarAddrs, sizeof(tU32S));
        }
    }

    return stsCode;
}

tU32 rtdb_write_tF32S( tF32S* VarAddrs, tF32 NewVal )
{
    tU32 stsCode = 0;
    tF32 valToWrite = VarAddrs->tF32_def;
    // check CRC
    if (rtdb_checkCrc32(VarAddrs, sizeof(VarAddrs)))
    {
        // TODO
    }
    // check for MIN
    else if ( NewVal < VarAddrs->tF32_min)
    {
        // TODO: Report error
        stsCode = 2;
    }
    // check for MAX
    else if ( NewVal > VarAddrs->tF32_max)
    {
        // TODO: Report error
        stsCode = 3;
    }
    else
    {
        if (OBJECT_STANDARD == VarAddrs->ss.objectStatus)
        {
            VarAddrs->tF32_val = NewVal;
            rtdb_calcCrc32( VarAddrs, sizeof(tF32S));
        }
    }

    return stsCode;
}

tU32 rtdb_write_tES( tES* VarAddrs, tE NewVal )
{
    tU32 stsCode = 0;
    tE valToWrite = VarAddrs->tE_def;
    // check CRC
    if (rtdb_checkCrc32(VarAddrs, sizeof(VarAddrs)))
    {
        // TODO
    }
    // check for MIN
    else if ( NewVal < VarAddrs->tE_min)
    {
        // TODO: Report error
        stsCode = 2;
    }
    // check for MAX
    else if ( NewVal > VarAddrs->tE_max)
    {
        // TODO: Report error
        stsCode = 3;
    }
    else
    {
        if (OBJECT_STANDARD == VarAddrs->ss.objectStatus)
        {
            VarAddrs->tE_val = NewVal;
            rtdb_calcCrc32( VarAddrs, sizeof(tES));
        }
    }

    return stsCode;
}

tU32 rtdb_overwrite_tS16S( tS16S* VarAddrs, tS16 NewVal )
{
    tU32 stsCode = 0;
    tS16 valToWrite = VarAddrs->tS16_def;
    // check CRC
    if (rtdb_checkCrc32( VarAddrs, sizeof(VarAddrs))) // TODO
    {
        // TODO
        stsCode = 1;
    }
    else
    {
        valToWrite = NewVal;
        VarAddrs->ss.objectStatus = OBJECT_OVERRIDDEN;
    }

    VarAddrs->tS16_val = valToWrite;

    //Recalculate CRC32
    rtdb_calcCrc32( VarAddrs, sizeof(tS16S));
    return stsCode;
}

tU32 rtdb_overwrite_tS32S( tS32S* VarAddrs, tS32 NewVal )
{
    tU32 stsCode = 0;
    tS32 valToWrite = VarAddrs->tS32_def;
    // check CRC
    if (rtdb_checkCrc32( VarAddrs, sizeof(VarAddrs))) // TODO
    {
        // TODO
        stsCode = 1;
    }
    else
    {
        valToWrite = NewVal;
        VarAddrs->ss.objectStatus = OBJECT_OVERRIDDEN;
    }

    VarAddrs->tS32_val = valToWrite;

    //Recalculate CRC32
    rtdb_calcCrc32( VarAddrs, sizeof(tS32S));
    return stsCode;
}

tU32 rtdb_overwrite_tU8S( tU8S* VarAddrs, tU8 NewVal )
{
    tU32 stsCode = 0;
    tU8 valToWrite = VarAddrs->tU8_def;
    // check CRC
    if (rtdb_checkCrc32( VarAddrs, sizeof(VarAddrs))) // TODO
    {
        // TODO
        stsCode = 1;
    }
    else
    {
        valToWrite = NewVal;
        VarAddrs->ss.objectStatus = OBJECT_OVERRIDDEN;
    }

    VarAddrs->tU8_val = valToWrite;

    //Recalculate CRC32
    rtdb_calcCrc32( VarAddrs, sizeof(tU8S));
    return stsCode;
}

tU32 rtdb_overwrite_tU32S( tU32S* VarAddrs, tU32 NewVal )
{
    tU32 stsCode = 0;
    tU32 valToWrite = VarAddrs->tU32_def;
    // check CRC
    if (rtdb_checkCrc32( VarAddrs, sizeof(VarAddrs))) // TODO
    {
        // TODO
        stsCode = 1;
    }
    else
    {
        valToWrite = NewVal;
        VarAddrs->ss.objectStatus = OBJECT_OVERRIDDEN;
    }

    VarAddrs->tU32_val = valToWrite;

    //Recalculate CRC32
    rtdb_calcCrc32( VarAddrs, sizeof(tU32S));
    return stsCode;
}

tU32 rtdb_overwrite_tF32S( tF32S* VarAddrs, tF32 NewVal )
{
    tU32 stsCode = 0;
    tF32 valToWrite = VarAddrs->tF32_def;
    // check CRC
    if (rtdb_checkCrc32( VarAddrs, sizeof(VarAddrs))) // TODO
    {
        // TODO
        stsCode = 1;
    }
    else
    {
        valToWrite = NewVal;
        VarAddrs->ss.objectStatus = OBJECT_OVERRIDDEN;
    }

    VarAddrs->tF32_val = valToWrite;

    //Recalculate CRC32
    rtdb_calcCrc32( VarAddrs, sizeof(tF32S));
    return stsCode;
}

tU32 rtdb_overwrite_tES( tES* VarAddrs, tE NewVal )
{
    tU32 stsCode = 0;
    tE valToWrite = VarAddrs->tE_def;
    // check CRC
    if (rtdb_checkCrc32( VarAddrs, sizeof(VarAddrs))) // TODO
    {
        // TODO
        stsCode = 1;
    }
    else
    {
        valToWrite = NewVal;
        VarAddrs->ss.objectStatus = OBJECT_OVERRIDDEN;
    }

    VarAddrs->tE_val = valToWrite;

    //Recalculate CRC32
    rtdb_calcCrc32( VarAddrs, sizeof(tES));
    return stsCode;
}

tU32 rtdb_releaseOverwrite_tS16S( tS16S* VarAddrs )
{
    tU32 stsCode = 0;
    // check CRC
    if (0) // TODO
    {
        // TODO
        stsCode = 1;
    }
    else
    {
        VarAddrs->ss.objectStatus = OBJECT_STANDARD;
        // TODO: Recalculate CRC
    }

    return stsCode;
}

tU32 rtdb_releaseOverwrite_tS32S( tS32S* VarAddrs )
{
    tU32 stsCode = 0;
    // check CRC
    if (0) // TODO
    {
        // TODO
        stsCode = 1;
    }
    else
    {
        VarAddrs->ss.objectStatus = OBJECT_STANDARD;
        // TODO: Recalculate CRC
    }

    return stsCode;
}

tU32 rtdb_releaseOverwrite_tU8S( tU8S* VarAddrs )
{
    tU32 stsCode = 0;
    // check CRC
    if (0) // TODO
    {
        // TODO
        stsCode = 1;
    }
    else
    {
        VarAddrs->ss.objectStatus = OBJECT_STANDARD;
        // TODO: Recalculate CRC
    }

    return stsCode;
}

tU32 rtdb_releaseOverwrite_tU32S( tU32S* VarAddrs )
{
    tU32 stsCode = 0;
    // check CRC
    if (0) // TODO
    {
        // TODO
        stsCode = 1;
    }
    else
    {
        VarAddrs->ss.objectStatus = OBJECT_STANDARD;
        // TODO: Recalculate CRC
    }

    return stsCode;
}

tU32 rtdb_releaseOverwrite_tF32S( tF32S* VarAddrs )
{
    tU32 stsCode = 0;
    // check CRC
    if (0) // TODO
    {
        // TODO
        stsCode = 1;
    }
    else
    {
        VarAddrs->ss.objectStatus = OBJECT_STANDARD;
        // TODO: Recalculate CRC
    }

    return stsCode;
}

tU32 rtdb_releaseOverwrite_tES( tES* VarAddrs )
{
    tU32 stsCode = 0;
    // check CRC
    if (0) // TODO
    {
        // TODO
        stsCode = 1;
    }
    else
    {
        VarAddrs->ss.objectStatus = OBJECT_STANDARD;
        // TODO: Recalculate CRC
    }

    return stsCode;
}

tS16S rtdb_read_tS16S( tS16S* VarAddrs )
{
    tS16S toReturn = *VarAddrs;
    // Check CRC
    if (0)
    {
        // TODO: implement CRC failed case
    }

    return toReturn;
}

tS32S rtdb_read_tS32S( tS32S* VarAddrs )
{
    tS32S toReturn = *VarAddrs;
    // Check CRC
    if (0)
    {
        // TODO: implement CRC failed case
    }

    return toReturn;
}

tU8S rtdb_read_tU8S( tU8S* VarAddrs )
{
    tU8S toReturn = *VarAddrs;
    // Check CRC
    if (0)
    {
        // TODO: implement CRC failed case
    }

    return toReturn;
}

tU32S rtdb_read_tU32S( tU32S* VarAddrs )
{
    tU32S toReturn = *VarAddrs;
    // Check CRC
    if (0)
    {
        // TODO: implement CRC failed case
    }

    return toReturn;
}

tF32S rtdb_read_tF32S( tF32S* VarAddrs )
{
    tF32S toReturn = *VarAddrs;
    // Check CRC
    if (0)
    {
        // TODO: implement CRC failed case
    }

    return toReturn;
}

tES rtdb_read_tES( tES* VarAddrs )
{
    tES toReturn = *VarAddrs;
    // Check CRC
    if (0)
    {
        // TODO: implement CRC failed case
    }

    return toReturn;
}