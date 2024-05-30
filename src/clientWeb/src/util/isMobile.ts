export function is_mobile(screenWidth: number): Boolean {
    return screenWidth <= 900
      ? true// 移动端参数
      : false; // PC端参数
  }