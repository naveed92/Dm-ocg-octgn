package dm_sets_extractor;

import java.awt.Image;
import java.awt.image.RenderedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import javax.imageio.ImageIO;

public class MainClass {

    public static void main(String args[]) {
        try {
           SinnanSetExtractor extractor = new SinnanSetExtractor();
           extractor.extractSet("", false); //optional to put the set name here. Exactly the address as it shows in the wikia url of the page.
     
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}
