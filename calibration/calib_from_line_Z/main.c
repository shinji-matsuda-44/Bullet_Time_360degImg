/* ************************************************************** main.c *** *
 * 直線の対応からカメラの回転行列を計算するプログラム
 *
 * Copyright (C) 2019 Yasuyuki SUGAYA <sugaya@iim.cs.tut.ac.jp>
 * Editor 2023 Shinji Matsuda
 *
 *                                    Time-stamp: <2023-06-05 16:34:27 iim-staff>
 * ************************************************************************* */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Eigen/Dense>
#include "getargs.h"
#include "common.h"
#include "calib.h"
#include <sys/stat.h>

#if 0
  R(0, 0) = 0.0;
  R(1, 0) = 0.0;
  R(2, 0) =-1.0;

  R(0, 1) = 1.0;
  R(1, 1) = 0.0;
  R(2, 1) = 0.0;

  R(0, 2) = 0.0;
  R(1, 2) =-1.0;
  R(2, 2) = 0.0;

  R(0, 0) = 1.0;
  R(1, 0) = 0.0;
  R(2, 0) = 0.0;

  R(0, 1) = 0.0;
  R(1, 1) = 1.0;
  R(2, 1) = 0.0;

  R(0, 2) = 0.0;
  R(1, 2) = 0.0;
  R(2, 2) = 1.0;

  R(0, 0) = 1.0;
  R(1, 0) = 0.0;
  R(2, 0) = 0.0;

  R(0, 1) = 0.0;
  R(1, 1) =-1.0;
  R(2, 1) = 0.0;

  R(0, 2) = 0.0;
  R(1, 2) = 0.0;
  R(2, 2) =-1.0;

  R(0, 0) = 0.0;
  R(1, 0) = 1.0;
  R(2, 0) = 0.0;

  R(0, 1) = 1.0;
  R(1, 1) = 0.0;
  R(2, 1) = 0.0;

  R(0, 2) = 0.0;
  R(1, 2) = 0.0;
  R(2, 2) =-1.0;
#endif


/* メイン関数 ************************************************************** */
int
main (int	argc,
      char*     argv[]) 
{
  /* 引数のチェック */
  Argument	*arg;
  if (!getargs (argc, argv, &arg)) usage (arg, argv[0]);

  /* カメラ行列を保存するファイル名 */
  char* output_folder_name = arg->output_folder_name;

  /* 対応線データの読み込み */
  Eigen::MatrixXd nV, dV, P;
  read_image_line (arg->image_line, nV);
  read_space_line (arg->space_line, dV, P);

  Eigen::MatrixXd R = Eigen::MatrixXd::Identity (3, 3);

  // カメラ姿勢の初期値 1,2,3
  /*
  R(0, 0) =-1.0;
  R(1, 0) = 0.0;
  R(2, 0) = 0.0;

  R(0, 1) = 0.0;
  R(1, 1) = 0.0;
  R(2, 1) =-1.0;

  R(0, 2) = 0.0;
  R(1, 2) =-1.0;
  R(2, 2) = 0.0;
  */

  // カメラ姿勢の初期値 4,5,6
  
  R(0, 0) = 0.0;
  R(1, 0) = 0.0;
  R(2, 0) =-1.0;

  R(0, 1) = 1.0;
  R(1, 1) = 0.0;
  R(2, 1) = 0.0;

  R(0, 2) = 0.0;
  R(1, 2) =-1.0;
  R(2, 2) = 0.0;
  
  

  // カメラ姿勢の初期値 7,8,9
  /*
  R(0, 0) = 1.0;
  R(1, 0) = 0.0;
  R(2, 0) = 0.0;

  R(0, 1) = 0.0;
  R(1, 1) = 0.0;
  R(2, 1) = 1.0;

  R(0, 2) = 0.0;
  R(1, 2) =-1.0;
  R(2, 2) = 0.0;
  */
  
  

  Eigen::VectorXd t = Eigen::VectorXd::Zero(3);

  /* カメラ姿勢の計算 */
  calc_motion (nV, dV, P, R, t, arg->eps);
  
  /* 結果の出力 */
  fprintf (stdout,
	   "%.16e %.16e %.16e\n%.16e %.16e %.16e\n%.16e %.16e %.16e\n"
	   "%.16e %.16e %.16e\n",
	   R(0, 0), R(0, 1), R(0, 2),
	   R(1, 0), R(1, 1), R(1, 2),
	   R(2, 0), R(2, 1), R(2, 2),
	   t(0), t(1), t(2));

  /* 世界座標系に対するカメラ位置を出力 */
  Eigen::VectorXd C = -R.transpose() * t;
  fprintf (stderr,
	   "Camera position is (%.16e %.16e %.16e).\n",
  	   C(0), C(1), C(2));

  /* データ保存用のフォルダを作成 */
  if (mkdir(output_folder_name, 0777) == 0) {
      printf("make folder\n");
  } else {
      printf("same folder already exist!\n");
  }

  //フォルダ名が長いとオーバーフローするので注意
  char file_path[50];

  /* 回転行列をtxtファイルに保存 */
  strcpy(file_path, output_folder_name);
  strcat(file_path, "/rotation_matrix.txt");
  FILE *file = fopen(file_path, "w");
  fprintf (file,
	   "%.16e, %.16e, %.16e\n%.16e, %.16e, %.16e\n%.16e, %.16e, %.16e\n",
	   R(0, 0), R(0, 1), R(0, 2),
	   R(1, 0), R(1, 1), R(1, 2),
	   R(2, 0), R(2, 1), R(2, 2)
     );
  memset(file_path, 0, sizeof(file_path)); //バッファをゼロでクリア

  /* 並進ベクトルをtxtファイルに保存 */
  strcpy(file_path, output_folder_name);
  strcat(file_path, "/translation_vector.txt");
  file = fopen(file_path, "w");
  fprintf (file,
    "%.16e, %.16e, %.16e\n",
    t(0), t(1), t(2)
    );
  memset(file_path, 0, sizeof(file_path)); //バッファをゼロでクリア

  /* 外部パラメータ行列をtxtファイルに保存 */
  strcpy(file_path, output_folder_name);
  strcat(file_path, "/external_matrix.txt");
  file = fopen(file_path, "w");
  fprintf (file,
	   "%.16e, %.16e, %.16e, %.16e\n%.16e, %.16e, %.16e, %.16e\n%.16e, %.16e, %.16e, %.16e\n",
	   R(0, 0), R(0, 1), R(0, 2), t(0),
	   R(1, 0), R(1, 1), R(1, 2), t(1),
	   R(2, 0), R(2, 1), R(2, 2), t(2)
	   );
  memset(file_path, 0, sizeof(file_path)); //バッファをゼロでクリア

  /* カメラ位置をtxtファイルに保存 */
  strcpy(file_path, output_folder_name);
  strcat(file_path, "/camera_position.txt");
  file = fopen(file_path, "w");
  fprintf (file,
	   "%.16e, %.16e, %.16e\n",
  	   C(0), C(1), C(2));
  memset(file_path, 0, sizeof(file_path)); //バッファをゼロでクリア
  
  /* 後始末 */
  argument_free (arg);
  
  return 0;
}

/* ******************************************************* End of main.c *** */
