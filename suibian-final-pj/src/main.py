from lightfield import *

if __name__ == "__main__":
  for i, arg in enumerate(sys.argv):
    lf = Lightfield("../scene/" + image_name + "/")
    alpha = -2
    for i in range(9):
      print("writing image with alpha =", alpha)
      ret = lf.refocus(alpha)
      sys.stdout.write("\nWriting to the disk buffer...")
      plt.imsave("./results/" + image_name + "/" + image_name + str(i) + " " + str(alpha) + ".png", ret)
      sys.stdout.write("\nRefocused with alpha = " + str(alpha) + " has ready!\n")
      alpha += 0.5
