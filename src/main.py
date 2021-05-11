from lightfield import *

if __name__ == "__main__":
  for i, arg in enumerate(sys.argv[1:]):
    image_name = arg
    lf = Lightfield("../scene/" + image_name + "/", image_name)
    alpha = -1.5
    # for i in range(9):
    #   print("writing image with alpha =", alpha)
    #   ret = lf.refocus(alpha)
    #   sys.stdout.write("\nWriting to the disk buffer...")
    #   plt.imsave("./results/" + image_name + "/" + image_name + str(i) + " " + str(alpha) + ".png", ret)
    #   sys.stdout.write("\nRefocused with alpha = " + str(alpha) + " has ready!\n")
    #   alpha += 0.5
    #
    # for i in range(9):
    #     print("now is doing apeture with", i, "radius")
    #     ret = lf.apeture(i)
    #     sys.stdout.write("Writing to the disk buffer...\n")
    #     plt.imsave("./results/" + image_name + "/apeture_" + str(i) + "_" + image_name  + ".png", ret)
    #     sys.stdout.write("Apeture with radius = " + str(i) + " has ready!\n")

    for i in range(11):
        radius = 8
        print("writing image with alpha =", i)
        ret = lf.combine(alpha, radius)
        sys.stdout.write("\nWriting to the disk buffer...")
        plt.imshow(ret)
        # plt.show()
        plt.imsave("./results/" + image_name + "/" + image_name + str(i) + " " + str(alpha) + " " + str(radius) + ".png", ret)
        sys.stdout.write("\nRefocused with alpha = " + str(alpha) + " has ready!\n")
        alpha += 0.5

    # for i in range(9):
    #     radius = i
    #     alpha = 2.2
    #     print("writing image with alpha =", i)
    #     ret = lf.combine(alpha, radius)
    #     sys.stdout.write("\nWriting to the disk buffer...")
    #     plt.imshow(ret)
    #     # plt.show()
    #     plt.imsave("./results/" + image_name + "/" + image_name + str(i) + " " + str(alpha) + " " + str(radius) + ".png", ret)
    #     sys.stdout.write("\nRefocused with alpha = " + str(alpha) + " has ready!\n")
