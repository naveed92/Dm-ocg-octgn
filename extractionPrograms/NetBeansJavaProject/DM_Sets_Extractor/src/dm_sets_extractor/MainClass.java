package dm_sets_extractor;

import java.awt.Image;
import java.awt.image.RenderedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import javax.imageio.ImageIO;
import javax.swing.JOptionPane;

public class MainClass {

    public static void main(String args[]) {
        try {
            SinnanSetExtractor extractor = new SinnanSetExtractor();
            //System.out.println(extractor.extract("Yomi,_Humanity_God", "lol", false));
            int extractImages = JOptionPane.showConfirmDialog(null, "Extract images?", "Alert", 1);
            switch (extractImages) {
                case 0:
                    extractor.extractSet("", true); //optional to put the set name here. Exactly the address as it shows in the wikia url of the page.
                    break;
                case 1:
                    extractor.extractSet("", false);
                    break;
                default:
                    System.out.println("Extraction cancelled.");
                    break;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}
