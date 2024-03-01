/* *********************************************************** getargs.c *** *
 * 引数解析関数
 *
 * Copyright (C) 2015 Yasuyuki SUGAYA <sugaya@iim.cs.tut.ac.jp>
 * Editor 2023 Shinji Matsuda
 *
 *                                    Time-stamp: <2019-11-25 14:43:51 sugaya>
 * ************************************************************************* */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "getargs.h"

const char*  PROGRAM            = "calib_from_lines";
const char*  VERSION            = "1.0.0";
const double DEFAULT_EPS	= 1.0e-15;

/* 仕様表示 **************************************************************** */
void
usage (Argument	*arg,
       char	*cmd) {
  fprintf (stderr,
	   "\n"
	   "* ***************************************************************"
	   "********** *\n"
	   "* This program computes the rotation matrix from line corresp.\n"
	   "* ***************************************************************"
	   "********** *\n");
  fprintf (stderr,
	   "Usage:%s image_lines.dat space_lines.dat output_folder_name\n", cmd);
  fprintf (stderr,
	   "\t --eps #\t\t: parameter for convergence (default 1.0e-15.\n"   
	   "\t -h\t\t: Show Usage.\n"	   
	   "\t -v\t\t: Show Version.\n"
	   "* ***************************************************************"
	   "********** *\n");
  
  argument_free (arg);
  exit (1);
}

/* バージョン表示 ********************************************************** */
void
version (Argument	*arg) {
  fprintf (stderr, "%s Ver.%s\n", PROGRAM, VERSION);
  argument_free (arg);
  exit (1);
}

/* 引数用構造体の生成 ****************************************************** */
Argument*
argument_new (void) {
  Argument	*arg;

  arg = (Argument *) malloc (sizeof (Argument));

  arg->image_line = NULL;
  arg->space_line = NULL;
  arg->output_folder_name = NULL;
  arg->eps        = DEFAULT_EPS;
  
  return arg;
}

/* 引数用構造体のメモリ解放 ************************************************ */
void
argument_free (Argument	*arg) {
  free (arg);
}

/* 引数のチェック ********************************************************** */
int
getargs (int		argc,
 	 char		**argv,
	 Argument	**arg) {
  int 	args;

  *arg = argument_new ();
  
  for (args = 1; args < argc; ++args) {
    if ((*argv[args] == '-') && *(argv[args]+1)) {
      if ((strcmp ("h", ++argv[args])) == 0) {
	      usage (*arg, argv[0]);
      } 
      else if ((strcmp ("v", argv[args])) == 0) {
	      version (*arg);
      } 
      else if ((strcmp ("-eps", argv[args])) == 0) {
	      if (++args >= argc) return 0;
	      (*arg)->eps = atof (argv[args]);
      }
    } 
    else {
      if (!((*arg)->image_line)) {
	      (*arg)->image_line = argv[args];
      } 
      else if (!((*arg)->space_line)) {
	      (*arg)->space_line = argv[args];
      }
      else if (!((*arg)->output_folder_name)) {
	      (*arg)->output_folder_name = argv[args];
      }
      else {
	      return 0;
      }
    }
  }
  if (!((*arg)->image_line) || !((*arg)->space_line) || !((*arg)->output_folder_name)) return 0;
  
  return 1;
}

/* **************************************************** End of getargs.c *** */
