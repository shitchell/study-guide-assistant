# Server API
can i haz json?

## search
Search for a quiz guide word or phrase

### parameters
parameter | type | description
--------- | ---- | -----------
q | string | A word or phrase to search and match against
results | integer | The maximum number of results to provide (default: 3, max: 10)

### example
```curl 'https://server.com/search?results=2&q=What%20is%20the%20First%20Amendment'```
```
{
  "query": "What is the First Amendment",
  "results": [
    {
      "term": "What is the First Amendment?",
      "definition": "Congress shall make no law respecting an establishment of religion, or prohibiting the exercise thereof; or abridging the freedom of speech, or of the press; or the right of the people peaceably to assemble, and to petition the government for a redress of grievances.",
      "timestamp": 1423152984,
      "ref": "https://quizlet.com/69859163/chapter-2-the-first-amendment-flash-cards/"
    },
    {
      "term": "What is the first amendment?",
      "definition": "Congress shall make no law abridging the freedom of speech or of the press",
      "timestamp": 1474516173,
      "ref": "https://quizlet.com/153555325/chapter-2-first-amendment-core-values-of-free-speech-flash-cards/"
    }
  ]
}
```
