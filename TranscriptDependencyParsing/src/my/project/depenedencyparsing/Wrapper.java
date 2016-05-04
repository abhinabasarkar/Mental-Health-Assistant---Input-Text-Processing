package my.project.depenedencyparsing;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import edu.stanford.nlp.trees.TypedDependency;

/**
 * Running class
 * @author abhi
 *
 */
public class Wrapper 
{
	public static String inputFile = "/home/abhi/Dropbox/IIITCoursework/Sem4/Project/DependencyParsing/transcript7.txt";
	public static String opFile = "/home/abhi/Dropbox/IIITCoursework/Sem4/Project/DependencyParsing/transcript7-op.txt";
	public static String subjObjFile = "/home/abhi/Dropbox/IIITCoursework/Sem4/Project/DependencyParsing/transcript7-subj-obj.txt";

	public static void main(String[] args) 
	{
		DepParser parser = new DepParser();
		try (BufferedReader inputReader = new BufferedReader(new FileReader(inputFile));
				BufferedWriter bwSubjects = new BufferedWriter(new FileWriter(subjObjFile, false));
				BufferedWriter bwOutput = new BufferedWriter(new FileWriter(opFile, false));)
		{
			for(String line; (line = inputReader.readLine()) != null; ) 
			{
				List<List<TypedDependency>> dependencies = parser.processText(line);
				
				// write the actual line to the file
				bwSubjects.write(line);
				bwSubjects.newLine();
				
				for (List<TypedDependency> sentence : dependencies)
				{
					// write the tagged text to the output file
					bwOutput.write(sentence.toString());
					bwOutput.newLine();
					
					List<TypedDependency> subjects = new ArrayList<TypedDependency> ();
					List<TypedDependency> objects = new ArrayList<TypedDependency> ();
					
					// for each dependency in the sentence
					for (TypedDependency dependency : sentence)
					{
						String relation = dependency.reln().toString();
						if (relation.equals("nsubj") || relation.equals ("nsubjpass"))
						{
							subjects.add(dependency);
						}
						else if (relation.equals("dobj"))
						{
							objects.add(dependency);
						}
					}
					
					bwSubjects.write ("Subjects - ");
					for (TypedDependency dependency : subjects)
					{
						bwSubjects.write (dependency.dep().word() + ", ");
					}
					
					bwSubjects.newLine();
					bwSubjects.write ("Objects - ");
					for (TypedDependency dependency : objects)
					{
						bwSubjects.write (dependency.dep().word() + ", ");
					}
					bwSubjects.newLine();
					bwSubjects.newLine();
				}
				bwSubjects.write("------------------------------------------------------\n\n");
		    }
		} 
		catch (IOException e) 
		{
			e.printStackTrace();
		}
	}


}
