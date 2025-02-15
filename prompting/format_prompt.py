instructions = """
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema 
{
"properties": 
    {
    "foo": 
        {
            "title": "Foo", 
            "description": "a list of strings", 
            "type": "array", 
            "items": 
                {"type": "string"}
        }
    }, 
    "required": ["foo"]
}

the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. 

The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:

```

{
"properties": 
    {
    "flag_law": {"title": "Flag Law", "type": "boolean"}, 
    "label": {"title": "Label", "type": "string"}, 
    "corpus": {"title": "Corpus", "type": "string"}, 
    "institution": {"title": "Institution", "type": "string"}, 
    "law_type": {"title": "Law Type", "type": "string"}, 
    "location": {"title": "Location", "type": "string"}, 
    "date": {"title": "Date", "type": "string"}}, 
"required": ["flag_law", "label", "corpus", "institution", "law_type", "location", "date"]
}
```

"""