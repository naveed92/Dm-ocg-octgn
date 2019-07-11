package dm_sets_extractor;

import javax.swing.JOptionPane;

public class MainClass {

    public static void main(String args[]) {
        try {
            SinnanSetExtractor extractor = new SinnanSetExtractor();
            System.out.println(extractor.extract("Metal_Avenger_Solid,_Dragon_Edge", "lol", false));
//            int extractImages = JOptionPane.showConfirmDialog(null, "Extract images?", "Alert", 1);
//            switch (extractImages) {
//                case 0:
//                    extractor.extractSet("", true); //optional to put the set name here. Exactly the address as it shows in the wikia url of the page.
//                    break;
//                case 1:
//                    extractor.extractSet("", false);
//                    break;
//                default:
//                    System.out.println("Extraction cancelled.");
//                    break;
//            }

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}
