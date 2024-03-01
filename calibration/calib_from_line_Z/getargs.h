/* *********************************************************** getargs.h *** *
 * 引数解析関数 ヘッダファイル
 *
 * Copyright (C) 1998-2008 Yasuyuki SUGAYA <sugaya@iim.ics.tut.ac.jp>
 *
 *                                    Time-stamp: <2019-11-25 14:43:59 sugaya>
 * ************************************************************************* */
#ifndef	__COMMON_FUNC_GETARGS_H__
#define	__COMMON_FUNC_GETARGS_H__

/* ************************************************************************* *
 * 引数用の構造体
 * 	- プログラムに必要な引数に応じてメンバを変更してください -
 * ************************************************************************* */
typedef struct _Argument {
  char*		image_line;
  char*		space_line;  
  char*   output_folder_name;
  double	eps;
} Argument;

/* ************************************************************************* *
 * 関数
 * ************************************************************************* */

void		usage		(Argument	*arg,
				 char		*cmd);         /* 使い方表示 */
void		version 	(Argument	*arg); /* バージョン情報表示 */
void		argument_free	(Argument	*arg);         /* メモリ解放 */
Argument*	argument_new 	(void);                  /* 引数構造体の生成 */
int		getargs 	(int		argc,        /* 引数解析関数 */
				 char		**argv,
				 Argument	**arg);

#endif	/* __COMMON_FUNC_GETARGS_H__ */

/* **************************************************** End of getargs.h *** */
