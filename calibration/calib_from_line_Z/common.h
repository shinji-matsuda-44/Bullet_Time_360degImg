/* ************************************************************ common.h *** *
 * �ͱ��Ѵ��׻��˶��̤���ؿ� �ء����ե�����
 *
 * Copyright (C) 2015 Yasuyuki SUGAYA <sugaya@iim.cs.tut.ac.jp>
 *
 *                                    Time-stamp: <2019-11-12 16:09:48 sugaya>
 * ************************************************************************* */
#ifndef	__HOMOGRAPHY_COMMON_H__
#define	__HOMOGRAPHY_COMMON_H__

#include <vector>

/* ************************************************************************* */
void	read_image_line	(char*			filename,
			 Eigen::MatrixXd& 	X);

void	read_space_line	(char*			filename,
			 Eigen::MatrixXd& 	X,
			 Eigen::MatrixXd&	P);

#endif /* __HOMOGRAPHY_COMMON_H__ */

/* ***************************************************** End of common.h *** */
