/* *********************************************************** getargs.h *** *
 * $B0z?t2r@O4X?t(B $B%X%C%@%U%!%$%k(B
 *
 * Copyright (C) 1998-2008 Yasuyuki SUGAYA <sugaya@iim.ics.tut.ac.jp>
 *
 *                                    Time-stamp: <2019-11-25 14:43:59 sugaya>
 * ************************************************************************* */
#ifndef	__COMMON_FUNC_GETARGS_H__
#define	__COMMON_FUNC_GETARGS_H__

/* ************************************************************************* *
 * $B0z?tMQ$N9=B$BN(B
 * 	- $B%W%m%0%i%`$KI,MW$J0z?t$K1~$8$F%a%s%P$rJQ99$7$F$/$@$5$$(B -
 * ************************************************************************* */
typedef struct _Argument {
  char*		image_line;
  char*		space_line;  
  char*   output_folder_name;
  double	eps;
} Argument;

/* ************************************************************************* *
 * $B4X?t(B
 * ************************************************************************* */

void		usage		(Argument	*arg,
				 char		*cmd);         /* $B;H$$J}I=<((B */
void		version 	(Argument	*arg); /* $B%P!<%8%g%s>pJsI=<((B */
void		argument_free	(Argument	*arg);         /* $B%a%b%j2rJ|(B */
Argument*	argument_new 	(void);                  /* $B0z?t9=B$BN$N@8@.(B */
int		getargs 	(int		argc,        /* $B0z?t2r@O4X?t(B */
				 char		**argv,
				 Argument	**arg);

#endif	/* __COMMON_FUNC_GETARGS_H__ */

/* **************************************************** End of getargs.h *** */
