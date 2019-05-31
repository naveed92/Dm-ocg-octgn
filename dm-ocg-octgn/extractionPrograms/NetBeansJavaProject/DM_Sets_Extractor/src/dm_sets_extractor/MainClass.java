package dm_sets_extractor;

import java.awt.Image;
import java.awt.image.RenderedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import javax.imageio.ImageIO;

public class MainClass {

    public static void main(String args[]) {

        /*
		String url = "http://duelmasters.wikia.com/wiki/File:dmr5-秘1.jpg";
		
		ImageExtractor extract = new ImageExtractor();
		
		try {
			String s = extract.extractImageUrl(url);
			System.out.println(s);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
         */
        try {
            //   Image pic = ImageIO.read(new URL("http://duelmasters.wikia.com/wiki/File:dmr5-秘1.jpg"));
            //    ImageIO.write((RenderedImage) pic, "jpg", new File("F:\\Duel\\ImageExtraction\\DMR05\\1111.jpg"));

           SinnanSetExtractor extractor = new SinnanSetExtractor();
           extractor.extractSet("", false); //optional to put the set name here. Exactly the address as it shows in the wikia url of the page.
      

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}
