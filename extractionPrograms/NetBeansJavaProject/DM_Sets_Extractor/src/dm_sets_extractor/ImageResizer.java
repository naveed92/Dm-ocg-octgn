package dm_sets_extractor;

import com.mortennobel.imagescaling.ResampleFilters;
import com.mortennobel.imagescaling.ResampleOp;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.awt.image.RenderedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;
import java.util.stream.Stream;
import javax.imageio.ImageIO;
import javax.swing.JOptionPane;
import javax.swing.JFileChooser;
import javax.swing.filechooser.FileNameExtensionFilter;

/**
 *
 * @author Pranjal This is for resizing images(with a pretty good filter) inside the given folder
 * 
 */
public class ImageResizer {

    int count = 0;

    public static void main(String args[]) throws Exception {
        ImageResizer temp = new ImageResizer();
        temp.doIt("DM-11_Eternal_Wave");

    }

    void doIt(String setName) throws Exception {
        try (Stream<Path> paths = Files.walk(Paths.get("F:\\Duel\\ImageExtraction\\Ivan Images\\final\\done"))) {
            paths
                    .filter(Files::isRegularFile)
                    .forEach(path -> {
                        if (!path.toString().contains("Proxies")) {
                            System.out.println(++count + " " + path);

                            File oldImage = new File(path.toString());
                            try {
                                BufferedImage pic = ImageIO.read(oldImage);
                                int width = pic.getWidth();
                                int height = pic.getHeight();
                                double aspect = (double) width / height;

                                ResampleOp resizeOp;
                                if (height > 561 || !path.toString().contains("Cards\\Crops")) {
                                    resizeOp = new ResampleOp((int) (aspect * 560), 560);
                                    resizeOp.setFilter(ResampleFilters.getLanczos3Filter());
                                    BufferedImage scaledPic = resizeOp.filter(pic, null);
                                    if (scaledPic.getType() == 6) {
                                        ImageIO.write((RenderedImage) scaledPic, "png", new File(path.toString()));
                                    } else {
                                        ImageIO.write((RenderedImage) scaledPic, "jpg", new File(path.toString()));
                                    }
                                } else {
                                   
                                    if (pic.getType() == 6) {
                                        ImageIO.write((RenderedImage) pic, "png", new File(path.toString()));
                                    } else {
                                        ImageIO.write((RenderedImage) pic, "jpg", new File(path.toString()));
                                    }
                                }

                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }
                    });
        }
    }

}
