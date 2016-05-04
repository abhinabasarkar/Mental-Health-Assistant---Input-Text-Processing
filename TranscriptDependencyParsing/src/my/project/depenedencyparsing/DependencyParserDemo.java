package my.project.depenedencyparsing;

import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.parser.nndep.DependencyParser;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.TypedDependency;

import java.io.StringReader;
import java.util.List;

/**
 * 
 * @author Abhi
 */

public class DependencyParserDemo 
{
	public static void main(String[] args) 
	{
		String modelPath = DependencyParser.DEFAULT_MODEL;
		String taggerPath = "edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger";

		String text = "Hmm. Well, how will this affect my work? I got a letter from Ms. Bows the other day. ";

		MaxentTagger tagger = new MaxentTagger(taggerPath);
		DependencyParser parser = DependencyParser.loadFromModelFile(modelPath);

		DocumentPreprocessor tokenizer = new DocumentPreprocessor(new StringReader(text));
		for (List<HasWord> sentence : tokenizer) 
		{
			List<TaggedWord> tagged = tagger.tagSentence(sentence);
			System.out.println(tagged);
			GrammaticalStructure gs = parser.predict(tagged);

			// Print typed dependencies
			List<TypedDependency> collection = (List<TypedDependency>) gs.typedDependencies();
			for (TypedDependency typedDependency : collection) 
			{
				System.out.println(typedDependency.gov());
				System.out.println(typedDependency.reln().getLongName());
				System.out.println(typedDependency.dep().word());
				System.out.println(typedDependency.dep().tag());
				System.out.println("------------");
			}
		}
	}
}
