#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _condrive_reg(void);
extern void _drive_reg(void);
extern void _exp2synNMDA_reg(void);
extern void _gap_reg(void);
extern void _gclamp_reg(void);
extern void _Gfluct_reg(void);
extern void _ka2_reg(void);
extern void _kdr_reg(void);
extern void _kv3_reg(void);
extern void _kv7_reg(void);
extern void _na_reg(void);
extern void _nas_reg(void);
extern void _spines_reg(void);
extern void _synapsesnodepression_reg(void);
extern void _synapseswithdepression_reg(void);
extern void _vecevent_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"mod/condrive.mod\"");
    fprintf(stderr, " \"mod/drive.mod\"");
    fprintf(stderr, " \"mod/exp2synNMDA.mod\"");
    fprintf(stderr, " \"mod/gap.mod\"");
    fprintf(stderr, " \"mod/gclamp.mod\"");
    fprintf(stderr, " \"mod/Gfluct.mod\"");
    fprintf(stderr, " \"mod/ka2.mod\"");
    fprintf(stderr, " \"mod/kdr.mod\"");
    fprintf(stderr, " \"mod/kv3.mod\"");
    fprintf(stderr, " \"mod/kv7.mod\"");
    fprintf(stderr, " \"mod/na.mod\"");
    fprintf(stderr, " \"mod/nas.mod\"");
    fprintf(stderr, " \"mod/spines.mod\"");
    fprintf(stderr, " \"mod/synapsesnodepression.mod\"");
    fprintf(stderr, " \"mod/synapseswithdepression.mod\"");
    fprintf(stderr, " \"mod/vecevent.mod\"");
    fprintf(stderr, "\n");
  }
  _condrive_reg();
  _drive_reg();
  _exp2synNMDA_reg();
  _gap_reg();
  _gclamp_reg();
  _Gfluct_reg();
  _ka2_reg();
  _kdr_reg();
  _kv3_reg();
  _kv7_reg();
  _na_reg();
  _nas_reg();
  _spines_reg();
  _synapsesnodepression_reg();
  _synapseswithdepression_reg();
  _vecevent_reg();
}

#if defined(__cplusplus)
}
#endif
