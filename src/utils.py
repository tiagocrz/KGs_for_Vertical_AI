def read_test_queries(file_path: str) -> list[str]:
    """
    Read test queries from a text file and return a list of questions.
    """
    questions = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
            raw_questions = content.split('\n\n')
            
            questions = [question.strip() for question in raw_questions]

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    return questions

