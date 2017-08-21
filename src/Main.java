import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;

/**
 * @author Derek
 *
 * Parses data from UniProt from the tab delimited form EntryID | Subcellular location [CC] to
 * EntryID | Type | ECO/PubMed
 */
public class Main {
	
	// list of UniProt IDs
	private static final ArrayList<String> ids = new ArrayList<String>();
	
	// list of types
	// Unrecognized
	// Single-pass transmembrane proteins
	// multi-pass transmembrane proteins
	// beta-barrel transmembrane proteins
	private static final ArrayList<String> types = new ArrayList<String>();
	
	// ECO/PubMed data
	private static final ArrayList<String> annotations = new ArrayList<String>();
	
	// the ascii of tab
	private static final int TAB = 9;
	
	// text descriptions of the types
	private static final String SINGLE = "Single-pass transmembrane protein", MULTI = "Multi-pass transmembrane protein", 
			BETA = "Beta-barrel transmembrane protein", UNKNOWN = "Data unknown";
	
	/**
	 * @param args - run time args
	 */
	public static void main(String[] args) {

		// open the file
		try (BufferedReader reader = new BufferedReader(new FileReader("res/data.tab"))) {

			// the current entry, skip the header
			String entry = reader.readLine();
			
			// read all entries in the list
			while ((entry = reader.readLine()) != null) {
				
				// the first column is the UniProtID
				ids.add(entry.substring(0, entry.indexOf(TAB)));
				
				// get the type
				if (entry.contains("Single-pass")) {
					types.add(SINGLE);
				} else if (entry.contains("Multi-pass")) {
					types.add(MULTI);
				} else if (entry.contains("Beta-barrel")) {
					types.add(BETA);
				} else {
					types.add(UNKNOWN);
				}
				
				// annotation data is inside of brackets
				if (entry.contains("{")) {
					annotations.add(entry.substring(entry.indexOf("{") + 1, entry.indexOf("}")));
				} else {
					annotations.add("");
				}
			}
			
			// an error occurred
		} catch (Exception e) {
			e.printStackTrace();
			return;
		}
		
		// now open the writer
		try (BufferedWriter writer = new BufferedWriter(new FileWriter("formatted_data.tab"))) {
			
			// print the header of the column
			writer.write(String.format("%s\t%7s\t%42s\n", "UniProtID", "Type", "Annotation"));
			
			for (int i = 0; i < ids.size(); i++) {
				
				// write the data in 3 columns
				writer.write(String.format("%10s\t%36s\t%s\n", ids.get(i), types.get(i), annotations.get(i)));
				
			}
			
			// an error occurred
		} catch (Exception e) {
			e.printStackTrace();
		}

	}

}
