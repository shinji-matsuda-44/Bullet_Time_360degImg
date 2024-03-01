/* ************************************************************ common.c *** *
 * 射影変換計算に共通する関数
 *
 * Copyright (C) 2019 Yasuyuki SUGAYA <sugaya@iim.cs.tut.ac.jp>
 * 
 *                                    Time-stamp: <2019-11-12 16:09:17 sugaya>
 * ************************************************************************* */
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <Eigen/Dense>

/* ************************************************************************* */
void
read_image_line (char*		  filename,
		 Eigen::MatrixXd& X) 
{
  FILE* fp = fopen (filename, "r");

  int nlines;
  fscanf (fp, "%d", &nlines);

  X.resize (3, nlines);
  for (int l = 0; l < nlines; l++) {
    double a, b, c;
    fscanf (fp, "%lf %lf %lf", &a, &b, &c);
    X(0, l) = a;
    X(1, l) = b;
    X(2, l) = c;
  }
  fclose (fp);
}

/* ************************************************************************* */
void
read_space_line (char*		  filename,
		 Eigen::MatrixXd& X,
		 Eigen::MatrixXd& P)
{
  FILE* fp = fopen (filename, "r");

  int nlines;
  fscanf (fp, "%d", &nlines);

  X.resize (3, nlines);
  P.resize (3, nlines);
  for (int l = 0; l < nlines; l++) {
    double a, b, c;
    fscanf (fp, "%lf %lf %lf", &a, &b, &c);
    X(0, l) = a;
    X(1, l) = b;
    X(2, l) = c;
    fscanf (fp, "%lf %lf %lf", &a, &b, &c);    
    P(0, l) = a;
    P(1, l) = b;
    P(2, l) = c;
  }
  fclose (fp);
}

/* ***************************************************** End of common.c *** */
