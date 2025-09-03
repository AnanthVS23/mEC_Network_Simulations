/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mech_api.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__naG
#define _nrn_initial _nrn_initial__naG
#define nrn_cur _nrn_cur__naG
#define _nrn_current _nrn_current__naG
#define nrn_jacob _nrn_jacob__naG
#define nrn_state _nrn_state__naG
#define _net_receive _net_receive__naG 
#define states states__naG 
#define trates trates__naG 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define gbar _p[0]
#define gbar_columnindex 0
#define thm1 _p[1]
#define thm1_columnindex 1
#define sigm1 _p[2]
#define sigm1_columnindex 2
#define km2 _p[3]
#define km2_columnindex 3
#define sigm2 _p[4]
#define sigm2_columnindex 4
#define kh1 _p[5]
#define kh1_columnindex 5
#define kh2 _p[6]
#define kh2_columnindex 6
#define sigh1 _p[7]
#define sigh1_columnindex 7
#define sigh2 _p[8]
#define sigh2_columnindex 8
#define thh2 _p[9]
#define thh2_columnindex 9
#define m _p[10]
#define m_columnindex 10
#define h _p[11]
#define h_columnindex 11
#define ina _p[12]
#define ina_columnindex 12
#define thegna _p[13]
#define thegna_columnindex 13
#define alpham _p[14]
#define alpham_columnindex 14
#define betam _p[15]
#define betam_columnindex 15
#define alphah _p[16]
#define alphah_columnindex 16
#define betah _p[17]
#define betah_columnindex 17
#define minf _p[18]
#define minf_columnindex 18
#define mtau _p[19]
#define mtau_columnindex 19
#define hinf _p[20]
#define hinf_columnindex 20
#define htau _p[21]
#define htau_columnindex 21
#define Dm _p[22]
#define Dm_columnindex 22
#define Dh _p[23]
#define Dh_columnindex 23
#define v _p[24]
#define v_columnindex 24
#define _g _p[25]
#define _g_columnindex 25
#define _ion_ina	*_ppvar[0]._pval
#define _ion_dinadv	*_ppvar[1]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_trates(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_naG", _hoc_setdata,
 "trates_naG", _hoc_trates,
 0, 0
};
 /* declare global and static user variables */
#define ena ena_naG
 double ena = 50;
#define eps eps_naG
 double eps = 1e-07;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "eps_naG", "mV",
 "ena_naG", "mV",
 "gbar_naG", "mho/cm2",
 "thm1_naG", "mV",
 "sigm1_naG", "mV",
 "sigm2_naG", "mV",
 "sigh1_naG", "mV",
 "sigh2_naG", "mV",
 "thh2_naG", "mV",
 0,0
};
 static double delta_t = 0.01;
 static double h0 = 0;
 static double m0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "eps_naG", &eps_naG,
 "ena_naG", &ena_naG,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(NrnThread*, _Memb_list*, int);
static void nrn_state(NrnThread*, _Memb_list*, int);
 static void nrn_cur(NrnThread*, _Memb_list*, int);
static void  nrn_jacob(NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(NrnThread*, _Memb_list*, int);
static void _ode_matsol(NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[2]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"naG",
 "gbar_naG",
 "thm1_naG",
 "sigm1_naG",
 "km2_naG",
 "sigm2_naG",
 "kh1_naG",
 "kh2_naG",
 "sigh1_naG",
 "sigh2_naG",
 "thh2_naG",
 0,
 0,
 "m_naG",
 "h_naG",
 0,
 0};
 static Symbol* _na_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 26, _prop);
 	/*initialize range parameters*/
 	gbar = 0.01;
 	thm1 = 1;
 	sigm1 = 4;
 	km2 = 0.1;
 	sigm2 = 13;
 	kh1 = 0.012;
 	kh2 = 0.2;
 	sigh1 = -20;
 	sigh2 = 3.5;
 	thh2 = 1;
 	_prop->param = _p;
 	_prop->param_size = 26;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_na_sym);
 	_ppvar[0]._pval = &prop_ion->param[3]; /* ina */
 	_ppvar[1]._pval = &prop_ion->param[4]; /* _ion_dinadv */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _na_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("na", -10000.);
 	_na_sym = hoc_lookup("na_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 1);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 26, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 naG /mnt/beegfs/home/avedur/NetPyNe_Sims/Automated/mEC_Network_Simulations/mod/na.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "naG";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int trates(_threadargsprotocomma_ double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static double *_temp1;
 static int _slist1[2], _dlist1[2];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {int _reset = 0; {
   trates ( _threadargscomma_ v ) ;
   Dm = ( minf - m ) / mtau ;
   Dh = ( hinf - h ) / htau ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
 trates ( _threadargscomma_ v ) ;
 Dm = Dm  / (1. - dt*( ( ( ( - 1.0 ) ) ) / mtau )) ;
 Dh = Dh  / (1. - dt*( ( ( ( - 1.0 ) ) ) / htau )) ;
  return 0;
}
 /*END CVODE*/
 
static int states (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {int _reset=0; int error = 0;
 {
   trates ( _threadargscomma_ v ) ;
   Dm = ( minf - m ) / mtau ;
   Dh = ( hinf - h ) / htau ;
   }
 return _reset;}
 
static int  trates ( _threadargsprotocomma_ double _lvm ) {
   alpham = - ( ( v - thm1 - eps ) / sigm1 ) / ( exp ( - ( v - thm1 - eps ) / sigm1 ) - 1.0 ) ;
   betam = km2 * exp ( - v / sigm2 ) ;
   mtau = 1.0 / ( alpham + betam ) ;
   minf = alpham / ( alpham + betam ) ;
   alphah = kh1 / exp ( - v / sigh1 ) ;
   betah = - kh2 * ( v - thh2 ) / ( exp ( - ( v - thh2 ) / sigh2 ) - 1.0 ) ;
   htau = 1.0 / ( alphah + betah ) ;
   hinf = alphah / ( alphah + betah ) ;
    return 0; }
 
static void _hoc_trates(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r = 1.;
 trates ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 2;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
     _ode_spec1 (_p, _ppvar, _thread, _nt);
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 2; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_na_sym, _ppvar, 0, 3);
   nrn_update_ion_pointer(_na_sym, _ppvar, 1, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
  int _i; double _save;{
  h = h0;
  m = m0;
 {
   trates ( _threadargscomma_ v ) ;
   }
 
}
}

static void nrn_init(NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
 initmodel(_p, _ppvar, _thread, _nt);
 }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   thegna = gbar * m * m * m * h ;
   ina = thegna * ( v - ena ) ;
   }
 _current += ina;

} return _current;
}

static void nrn_cur(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dina;
  _dina = ina;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dinadv += (_dina - ina)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ina += ina ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}
 
}

static void nrn_state(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
double _dtsav = dt;
if (secondorder) { dt *= 0.5; }
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
 {   euler_thread(2, _slist1, _dlist1, _p, states, _ppvar, _thread, _nt);
     if (secondorder) {
    int _i;
    for (_i = 0; _i < 2; ++_i) {
      _p[_slist1[_i]] += dt*_p[_dlist1[_i]];
    }}
 } }}
 dt = _dtsav;
}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = m_columnindex;  _dlist1[0] = Dm_columnindex;
 _slist1[1] = h_columnindex;  _dlist1[1] = Dh_columnindex;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/mnt/beegfs/home/avedur/NetPyNe_Sims/Automated/mEC_Network_Simulations/mod/na.mod";
static const char* nmodl_file_text = 
  "TITLE naG\n"
  ": Na current for axon. No slow inact.\n"
  ": M.Migliore Jul. 1997\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX naG\n"
  "	USEION na WRITE ina\n"
  "	RANGE  gbar,thm1,sigm1,km2,sigm2,kh1,kh2,sigh1,sigh2,thh2\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	gbar = 0.010   	(mho/cm2)	:this should be read in\n"
  "	eps=1e-7 (mV)\n"
  "	thm1=1	(mV) :this should be read in\n"
  "	sigm1=4 (mV)\n"
  "	km2=0.1\n"
  "	sigm2=13 (mV)\n"
  "	kh1=0.012\n"
  "	kh2=0.2\n"
  "	sigh1=-20 (mV)\n"
  "	sigh2=3.5 (mV)\n"
  "	thh2=1 (mV)	:this should be read in\n"
  "	:mmin=0.02	\n"
  "	:hmin=0.5	\n"
  "\n"
  "	ena=50		(mV)            : must be explicitly def. in hoc\n"
  "	celsius\n"
  "	v 		(mV)\n"
  "}\n"
  "\n"
  "\n"
  "UNITS {\n"
  "	(mV) = (millivolt)\n"
  "	(mA) = (milliamp)\n"
  "	(S) = (siemens)\n"
  "} \n"
  "\n"
  "ASSIGNED {\n"
  "	ina 		(mA/cm2)\n"
  "	thegna		(S/cm2) \n"
  "	alpham\n"
  "	betam\n"
  "	alphah\n"
  "	betah\n"
  "	minf	(ms)\n"
  "	mtau	(ms)\n"
  "	hinf\n"
  "	htau\n"
  "}\n"
  " \n"
  "\n"
  "STATE { m h}\n"
  "\n"
  "BREAKPOINT {\n"
  "        SOLVE states METHOD euler\n"
  "        thegna = gbar*m*m*m*h\n"
  "	ina = thegna * (v - ena)\n"
  "} \n"
  "\n"
  "INITIAL {\n"
  "	trates(v)\n"
  "}\n"
  "\n"
  "DERIVATIVE states {   \n"
  "        trates(v)      \n"
  "        m' = (minf-m)/mtau\n"
  "        h' = (hinf-h)/htau\n"
  "}\n"
  "\n"
  "PROCEDURE trates(vm) {  \n"
  "        \n"
  "    alpham = -((v-thm1-eps)/sigm1)/(exp(-(v-thm1-eps)/sigm1)-1)\n"
  "    betam = km2*exp(-v/sigm2)\n"
  "	\n"
  "	mtau = 1/(alpham+betam)\n"
  "	minf = alpham/(alpham+betam)\n"
  "\n"
  "	alphah = kh1/exp(-v/sigh1)\n"
  "    betah = -kh2*(v-thh2)/(exp(-(v-thh2)/sigh2)-1)\n"
  "	\n"
  "	htau =  1/(alphah+betah)\n"
  "    hinf = alphah/(alphah+betah)                 \n"
  "	\n"
  "}\n"
  "\n"
  "        \n"
  "\n"
  "        \n"
  "\n"
  ;
#endif
