package my.project.depenedencyparsing;

import java.io.StringReader;
import java.util.ArrayList;
import java.util.List;

import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.parser.nndep.DependencyParser;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.TypedDependency;

public class DepParser 
{
	private String modelPath;
	private String taggerPath;
	private MaxentTagger tagger;
	private DependencyParser parser;

	/**
	 * constructor
	 */
	public DepParser() 
	{
		this.modelPath = DependencyParser.DEFAULT_MODEL;
		this.taggerPath = "edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger";

		this.tagger = new MaxentTagger(taggerPath);
		this.parser = DependencyParser.loadFromModelFile(modelPath);
	}

	/**
	 * processes one line of transcript text, can contain multiple sentences
	 * @param text 
	 * @return TypedDependecies for each sentences
	 */
	List<List<TypedDependency>> processText (String text)
	{
		DocumentPreprocessor tokenizer = new DocumentPreprocessor(new StringReader(text));
		
		// the arraylist to be returned;
		List<List<TypedDependency>> ret = new ArrayList<List<TypedDependency>> ();	
		
		// for each sentence in the text
		for (List<HasWord> sentence : tokenizer) 
		{
			List<TaggedWord> tagged = tagger.tagSentence(sentence);
			GrammaticalStructure gs = parser.predict(tagged);

			// getting a list of the typed dependencies for the sentence
			List<TypedDependency> collection = (ArrayList<TypedDependency>) gs.typedDependencies();
			ret.add(collection);
		}
		
		return ret;
	}

}
