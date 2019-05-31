/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dm_sets_extractor;

/**
 *
 * @author Win7
 */
import java.io.*;

public class FormatAdder {

    public static void main(String args[]) throws IOException {

        String path = "C:\\Users\\Win7\\Documents\\NetBeansProjects\\DM_Sets_Extractor\\dm-ocg-octgn-master\\dm-ocg-octgn\\game\\Sets\\";
        File file = new File(path);
        String tempath = null;
        String format;
        String[] names = file.list();

        FileReader in = null;
        FileWriter out = null;

        BufferedReader r = null;
        BufferedWriter w = null;

        try {
            for (String name : names) {
                if (new File(path + "\\" + name).isDirectory()) {
                    tempath = path + "\\" + name + "\\";
                    System.out.println("path is " + tempath);
                }
                int count = 0;
                int i1 = name.indexOf("DM-");
                if (i1 == -1) {
                    break;
                } else {
                    i1 += 3;
                }

                int setNum = Integer.parseInt(name.substring(i1, i1 + 2));
                System.out.println("Setnum is=" + setNum);

                if (setNum <= 12) {
                    format = "TCG, Set17, Set35, OCG";
                } else if (setNum <= 17) {
                    format = "Set17, Set35, OCG";
                } else if (setNum <= 35) {
                    format = "Set35, OCG";
                } else {
                    format = "OCG";
                }

                in = new FileReader(tempath + "set.xml");
                out = new FileWriter(tempath + "setoutput.xml");

                r = new BufferedReader(in);
                w = new BufferedWriter(out);
                String line;

                while ((line = r.readLine()) != null) {
                    w.write(line + "\n");
                    if (line.contains("card name=") || line.contains("alternate name=")) {
                        w.write("\t\t\t<property name=\"Format\" value=\"" + format + "\" />");
                        w.newLine();
                        ++count;
                    }

                }
                System.out.println(name + "count=" + count);

                r.close();
                w.close();
                in.close();
                out.close();

            }

        } finally {
            r.close();
            w.close();
            if (in != null) {
                in.close();
            }
            if (out != null) {
                out.close();
            }
        }
    }
}
