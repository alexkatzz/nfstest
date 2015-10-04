#===============================================================================
# Copyright 2014 NetApp, Inc. All Rights Reserved,
# contribution by Jorge Mora <mora@netapp.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#===============================================================================
# Generated by process_xdr.py from nlm4.x on Sun Oct 04 08:09:28 2015
"""
NLMv4 decoding module
"""
import nfstest_config as c
import nlm4_const as const
from packet.utils import *
from baseobj import BaseObj
from packet.unpack import Unpack

# Module constants
__author__    = "Jorge Mora (%s)" % c.NFSTEST_AUTHOR_EMAIL
__copyright__ = "Copyright (C) 2014 NetApp, Inc."
__license__   = "GPL v2"
__version__   = "4.0"

#
# Constants
class nfs_bool(Enum):
    """enum nfs_bool"""
    _enumdict = const.nfs_bool

# Basic data types
uint64 = Unpack.unpack_uint64
int64  = Unpack.unpack_int64
uint32 = Unpack.unpack_uint
int32  = Unpack.unpack_int
nlm_fh = lambda unpack: StrHex(unpack.unpack_opaque(const.MAXNETOBJ_SZ))
netobj = lambda unpack: StrHex(unpack.unpack_opaque(const.MAXNETOBJ_SZ))
strobj = lambda unpack: unpack.unpack_opaque(const.MAXNETOBJ_SZ)

class nlm4_stats(Enum):
    """enum nlm4_stats"""
    _enumdict = const.nlm4_stats

class fsh4_mode(Enum):
    """enum fsh4_mode"""
    _enumdict = const.fsh4_mode

class fsh4_access(Enum):
    """enum fsh4_access"""
    _enumdict = const.fsh4_access

class nlm4_holder(BaseObj):
    """
       struct nlm4_holder {
           bool   exclusive;
           int32  svid;
           strobj oh;
           uint64 offset;
           uint64 length;
       };
    """
    # Class attributes
    _strfmt1  = "off:{3:umax64} len:{4:umax64} excl:{0}"
    _attrlist = ("exclusive", "svid", "oh", "offset", "length")

    def __init__(self, unpack):
        self.exclusive = nfs_bool(unpack)
        self.svid      = int32(unpack)
        self.oh        = strobj(unpack)
        self.offset    = uint64(unpack)
        self.length    = uint64(unpack)

class nlm4_lock(BaseObj):
    """
       struct nlm4_lock {
           string owner<LM_MAXSTRLEN>;
           nlm_fh fh;
           strobj oh;
           int32  svid;
           uint64 offset;
           uint64 length;
       };
    """
    # Class attributes
    _strfmt1  = "FH:{1:crc32} off:{4:umax64} len:{5:umax64}"
    _attrlist = ("owner", "fh", "oh", "svid", "offset", "length")

    def __init__(self, unpack):
        self.owner  = unpack.unpack_opaque(const.LM_MAXSTRLEN)
        self.fh     = nlm_fh(unpack)
        self.oh     = strobj(unpack)
        self.svid   = int32(unpack)
        self.offset = uint64(unpack)
        self.length = uint64(unpack)

class nlm4_share(BaseObj):
    """
       struct nlm4_share {
           string      owner<LM_MAXSTRLEN>;
           nlm_fh      fh;
           strobj      oh;
           fsh4_mode   mode;
           fsh4_access access;
       };
    """
    # Class attributes
    _strfmt1  = "FH:{1:crc32} owner:{0}"
    _attrlist = ("owner", "fh", "oh", "mode", "access")

    def __init__(self, unpack):
        self.owner  = unpack.unpack_opaque(const.LM_MAXSTRLEN)
        self.fh     = nlm_fh(unpack)
        self.oh     = strobj(unpack)
        self.mode   = fsh4_mode(unpack)
        self.access = fsh4_access(unpack)

class nlm4_testargs(BaseObj):
    """
       struct nlm4_testargs {
           netobj    cookie;
           bool      exclusive;
           nlm4_lock locker;
       };
    """
    # Class attributes
    _strfmt1  = "{2} excl:{1}"
    _attrlist = ("cookie", "exclusive", "locker")

    def __init__(self, unpack):
        self.cookie    = netobj(unpack)
        self.exclusive = nfs_bool(unpack)
        self.locker    = nlm4_lock(unpack)

class TEST4args(nlm4_testargs): pass
class TEST_MSG4args(nlm4_testargs): pass
class GRANTED4args(nlm4_testargs): pass
class GRANTED_MSG4args(nlm4_testargs): pass

class nlm4_testrply(BaseObj):
    """
       union switch nlm4_testrply (nlm4_stats status) {
           case const.NLM4_DENIED:
               nlm4_holder denied;
           default:
               void;
       };
    """
    # Class attributes
    _strfmt1 = "{0} {1}"

    def __init__(self, unpack):
        self.set_attr("status", nlm4_stats(unpack))
        if self.status == const.NLM4_DENIED:
            self.set_attr("denied", nlm4_holder(unpack), switch=True)

class nlm4_testres(BaseObj):
    """
       struct nlm4_testres {
           netobj        cookie;
           nlm4_testrply stat;
       };
    """
    # Class attributes
    _fattrs   = ("stat",)
    _strfmt1  = "{1}"
    _attrlist = ("cookie", "stat")

    def __init__(self, unpack):
        self.cookie = netobj(unpack)
        self.stat   = nlm4_testrply(unpack)

class TEST_RES4args(nlm4_testres): pass
class TEST4res(nlm4_testres): pass

class nlm4_lockargs(BaseObj):
    """
       struct nlm4_lockargs {
           netobj    cookie;
           bool      block;
           bool      exclusive;
           nlm4_lock locker;
           bool      reclaim;    /* used for recovering locks */
           int       state;      /* specify local status monitor state */
       };
    """
    # Class attributes
    _strfmt1  = "{3} excl:{2} block:{1}"
    _attrlist = ("cookie", "block", "exclusive", "locker", "reclaim", "state")

    def __init__(self, unpack):
        self.cookie    = netobj(unpack)
        self.block     = nfs_bool(unpack)
        self.exclusive = nfs_bool(unpack)
        self.locker    = nlm4_lock(unpack)
        self.reclaim   = nfs_bool(unpack)
        self.state     = unpack.unpack_int()

class LOCK4args(nlm4_lockargs): pass
class LOCK_MSG4args(nlm4_lockargs): pass
class NM_LOCK4args(nlm4_lockargs): pass

class nlm4_res(BaseObj):
    """
       struct nlm4_res {
           netobj     cookie;
           nlm4_stats status;
       };
    """
    # Class attributes
    _strfmt1  = "{1}"
    _attrlist = ("cookie", "status")

    def __init__(self, unpack):
        self.cookie = netobj(unpack)
        self.status = nlm4_stats(unpack)

class LOCK_RES4args(nlm4_res): pass
class CANCEL_RES4args(nlm4_res): pass
class UNLOCK_RES4args(nlm4_res): pass
class GRANTED_RES4args(nlm4_res): pass
class LOCK4res(nlm4_res): pass
class CANCEL4res(nlm4_res): pass
class UNLOCK4res(nlm4_res): pass
class GRANTED4res(nlm4_res): pass
class NM_LOCK4res(nlm4_res): pass

class nlm4_cancargs(BaseObj):
    """
       struct nlm4_cancargs {
           netobj    cookie;
           bool      block;
           bool      exclusive;
           nlm4_lock locker;
       };
    """
    # Class attributes
    _attrlist = ("cookie", "block", "exclusive", "locker")

    def __init__(self, unpack):
        self.cookie    = netobj(unpack)
        self.block     = nfs_bool(unpack)
        self.exclusive = nfs_bool(unpack)
        self.locker    = nlm4_lock(unpack)

class CANCEL4args(nlm4_cancargs): pass
class CANCEL_MSG4args(nlm4_cancargs): pass

class nlm4_unlockargs(BaseObj):
    """
       struct nlm4_unlockargs {
           netobj    cookie;
           nlm4_lock locker;
       };
    """
    # Class attributes
    _strfmt1  = "{1}"
    _attrlist = ("cookie", "locker")

    def __init__(self, unpack):
        self.cookie = netobj(unpack)
        self.locker = nlm4_lock(unpack)

class UNLOCK4args(nlm4_unlockargs): pass
class UNLOCK_MSG4args(nlm4_unlockargs): pass

class nlm4_shareargs(BaseObj):
    """
       struct nlm4_shareargs {
           netobj     cookie;
           nlm4_share share;
           bool       reclaim;
       };
    """
    # Class attributes
    _attrlist = ("cookie", "share", "reclaim")

    def __init__(self, unpack):
        self.cookie  = netobj(unpack)
        self.share   = nlm4_share(unpack)
        self.reclaim = nfs_bool(unpack)

class SHARE4args(nlm4_shareargs): pass
class UNSHARE4args(nlm4_shareargs): pass

class nlm4_shareres(BaseObj):
    """
       struct nlm4_shareres {
           netobj     cookie;
           nlm4_stats status;
           int        sequence;
       };
    """
    # Class attributes
    _attrlist = ("cookie", "status", "sequence")

    def __init__(self, unpack):
        self.cookie   = netobj(unpack)
        self.status   = nlm4_stats(unpack)
        self.sequence = unpack.unpack_int()

class SHARE4res(nlm4_shareres): pass
class UNSHARE4res(nlm4_shareres): pass

class FREE_ALL4args(BaseObj):
    """
       struct FREE_ALL4args {
           string name<MAXNAMELEN>;
           int32  state;
       };
    """
    # Class attributes
    _strfmt1  = "state:{1} name:{0}"
    _attrlist = ("name", "state")

    def __init__(self, unpack):
        self.name  = unpack.unpack_opaque(const.MAXNAMELEN)
        self.state = int32(unpack)

# Procedures
class nlm_proc4(Enum):
    """enum nlm_proc4"""
    _enumdict = const.nlm_proc4

class NLM4args(RPCload):
    """
       union switch NLM4args (nlm_proc4 procedure) {
           case const.NLMPROC4_NULL:
               void;
           case const.NLMPROC4_TEST:
               TEST4args optest;
           case const.NLMPROC4_LOCK:
               LOCK4args oplock;
           case const.NLMPROC4_CANCEL:
               CANCEL4args opcancel;
           case const.NLMPROC4_UNLOCK:
               UNLOCK4args opunlock;
           case const.NLMPROC4_GRANTED:
               GRANTED4args opgranted;
           case const.NLMPROC4_TEST_MSG:
               TEST_MSG4args optest_msg;
           case const.NLMPROC4_LOCK_MSG:
               LOCK_MSG4args oplock_msg;
           case const.NLMPROC4_CANCEL_MSG:
               CANCEL_MSG4args opcancel_msg;
           case const.NLMPROC4_UNLOCK_MSG:
               UNLOCK_MSG4args opunlock_msg;
           case const.NLMPROC4_GRANTED_MSG:
               GRANTED_MSG4args opgranted_msg;
           case const.NLMPROC4_TEST_RES:
               TEST_RES4args optest_res;
           case const.NLMPROC4_LOCK_RES:
               LOCK_RES4args oplock_res;
           case const.NLMPROC4_CANCEL_RES:
               CANCEL_RES4args opcancel_res;
           case const.NLMPROC4_UNLOCK_RES:
               UNLOCK_RES4args opunlock_res;
           case const.NLMPROC4_GRANTED_RES:
               GRANTED_RES4args opgranted_res;
           case const.NLMPROC4_SHARE:
               SHARE4args opshare;
           case const.NLMPROC4_UNSHARE:
               UNSHARE4args opunshare;
           case const.NLMPROC4_NM_LOCK:
               NM_LOCK4args opnm_lock;
           case const.NLMPROC4_FREE_ALL:
               FREE_ALL4args opfree_all;
       };
    """
    # Class attributes
    _pindex  = 9
    _strname = "NLM"

    def __init__(self, unpack, procedure):
        self.set_attr("procedure", nlm_proc4(procedure))
        if self.procedure == const.NLMPROC4_NULL:
            self.set_strfmt(2, "NULL()")
        elif self.procedure == const.NLMPROC4_TEST:
            self.set_attr("optest", TEST4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_LOCK:
            self.set_attr("oplock", LOCK4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_CANCEL:
            self.set_attr("opcancel", CANCEL4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_UNLOCK:
            self.set_attr("opunlock", UNLOCK4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_GRANTED:
            self.set_attr("opgranted", GRANTED4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_TEST_MSG:
            self.set_attr("optest_msg", TEST_MSG4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_LOCK_MSG:
            self.set_attr("oplock_msg", LOCK_MSG4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_CANCEL_MSG:
            self.set_attr("opcancel_msg", CANCEL_MSG4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_UNLOCK_MSG:
            self.set_attr("opunlock_msg", UNLOCK_MSG4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_GRANTED_MSG:
            self.set_attr("opgranted_msg", GRANTED_MSG4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_TEST_RES:
            self.set_attr("optest_res", TEST_RES4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_LOCK_RES:
            self.set_attr("oplock_res", LOCK_RES4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_CANCEL_RES:
            self.set_attr("opcancel_res", CANCEL_RES4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_UNLOCK_RES:
            self.set_attr("opunlock_res", UNLOCK_RES4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_GRANTED_RES:
            self.set_attr("opgranted_res", GRANTED_RES4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_SHARE:
            self.set_attr("opshare", SHARE4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_UNSHARE:
            self.set_attr("opunshare", UNSHARE4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_NM_LOCK:
            self.set_attr("opnm_lock", NM_LOCK4args(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_FREE_ALL:
            self.set_attr("opfree_all", FREE_ALL4args(unpack), switch=True)
        self.argop = self.procedure
        self.op    = self.procedure

class NLM4res(RPCload):
    """
       union switch NLM4res (nlm_proc4 procedure) {
           case const.NLMPROC4_NULL:
               void;
           case const.NLMPROC4_TEST:
               TEST4res optest;
           case const.NLMPROC4_LOCK:
               LOCK4res oplock;
           case const.NLMPROC4_CANCEL:
               CANCEL4res opcancel;
           case const.NLMPROC4_UNLOCK:
               UNLOCK4res opunlock;
           case const.NLMPROC4_GRANTED:
               GRANTED4res opgranted;
           case const.NLMPROC4_TEST_MSG:
               void;
           case const.NLMPROC4_LOCK_MSG:
               void;
           case const.NLMPROC4_CANCEL_MSG:
               void;
           case const.NLMPROC4_UNLOCK_MSG:
               void;
           case const.NLMPROC4_GRANTED_MSG:
               void;
           case const.NLMPROC4_TEST_RES:
               void;
           case const.NLMPROC4_LOCK_RES:
               void;
           case const.NLMPROC4_CANCEL_RES:
               void;
           case const.NLMPROC4_UNLOCK_RES:
               void;
           case const.NLMPROC4_GRANTED_RES:
               void;
           case const.NLMPROC4_SHARE:
               SHARE4res opshare;
           case const.NLMPROC4_UNSHARE:
               UNSHARE4res opunshare;
           case const.NLMPROC4_NM_LOCK:
               NM_LOCK4res opnm_lock;
           case const.NLMPROC4_FREE_ALL:
               void;
       };
    """
    # Class attributes
    _pindex  = 9
    _strname = "NLM"

    def __init__(self, unpack, procedure):
        self.set_attr("procedure", nlm_proc4(procedure))
        if self.procedure == const.NLMPROC4_NULL:
            self.set_strfmt(2, "NULL()")
        elif self.procedure == const.NLMPROC4_TEST:
            self.set_attr("optest", TEST4res(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_LOCK:
            self.set_attr("oplock", LOCK4res(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_CANCEL:
            self.set_attr("opcancel", CANCEL4res(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_UNLOCK:
            self.set_attr("opunlock", UNLOCK4res(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_GRANTED:
            self.set_attr("opgranted", GRANTED4res(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_TEST_MSG:
            self.set_strfmt(2, "TEST_MSG4res()")
        elif self.procedure == const.NLMPROC4_LOCK_MSG:
            self.set_strfmt(2, "LOCK_MSG4res()")
        elif self.procedure == const.NLMPROC4_CANCEL_MSG:
            self.set_strfmt(2, "CANCEL_MSG4res()")
        elif self.procedure == const.NLMPROC4_UNLOCK_MSG:
            self.set_strfmt(2, "UNLOCK_MSG4res()")
        elif self.procedure == const.NLMPROC4_GRANTED_MSG:
            self.set_strfmt(2, "GRANTED_MSG4res()")
        elif self.procedure == const.NLMPROC4_TEST_RES:
            self.set_strfmt(2, "TEST_RES4res()")
        elif self.procedure == const.NLMPROC4_LOCK_RES:
            self.set_strfmt(2, "LOCK_RES4res()")
        elif self.procedure == const.NLMPROC4_CANCEL_RES:
            self.set_strfmt(2, "CANCEL_RES4res()")
        elif self.procedure == const.NLMPROC4_UNLOCK_RES:
            self.set_strfmt(2, "UNLOCK_RES4res()")
        elif self.procedure == const.NLMPROC4_GRANTED_RES:
            self.set_strfmt(2, "GRANTED_RES4res()")
        elif self.procedure == const.NLMPROC4_SHARE:
            self.set_attr("opshare", SHARE4res(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_UNSHARE:
            self.set_attr("opunshare", UNSHARE4res(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_NM_LOCK:
            self.set_attr("opnm_lock", NM_LOCK4res(unpack), switch=True)
        elif self.procedure == const.NLMPROC4_FREE_ALL:
            self.set_strfmt(2, "FREE_ALL4res()")
        self.resop = self.procedure
        self.op    = self.procedure
