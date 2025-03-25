from OperaPowerRelay import opr
from FileWhisperer import FileWhisperer as fw
from deep_translator import GoogleTranslator
import traceback


"""
    WhisperTranslate is a script that works in conjunction with FileWhisperer to translate the 
    filename and metadata of files and directories
"""
TRANSLATOR = GoogleTranslator(source='auto', target='en')

def change_translator(source: str, target: str):
    global TRANSLATOR
    TRANSLATOR = GoogleTranslator(source=source, target=target)


def translate_with_metadata(file: fw.CleanFile) -> fw.CleanFile | None:
    
    try:
        translated_file_name = pure_translate(file.Name)
        if translated_file_name:
            file.Name = translated_file_name
        if any(file.Path.endswith(f) for f in fw.AUDIO_FORMATS):
            translated_audio_title = pure_translate(file.Metadata_dict["TITLE"]) 
            if translated_audio_title:
                file.Metadata_dict["TITLE"] = translated_audio_title
    # include logic to deal with other file formats here
        else:
            opr.print_from("WhisperTranslate - Translate with Metadata", f"{file.Name}'s file format is not supported")
                
        return file
    except Exception:
        error_message = traceback.format_exc()
        opr.print_from("WhisperTranslate - Translate with Metadata", f"FAILED: Unexpected Error while translating {file.Name}: {error_message}")
        return None

def pure_translate(word: str) -> str | None:
    global TRANSLATOR
    translate_word = TRANSLATOR.translate(word)
    if not translate_word:
        raise Exception
    return translate_word

def translate_files(files: list[fw.CleanFile | dict [str, list]]) -> list[fw.CleanFile | dict [str, list]]:
    
    translated: list[fw.CleanFile | dict [str, list]] = []
    for f in files:
        if isinstance(f, fw.CleanFile):
            _ = translate_with_metadata(f)
            if _:
                translated.append(_)
        elif isinstance(f, dict):
            subdirectory_name, subdirectory_items = next(iter(f.items()))
            translated.append({subdirectory_name: translate_files(subdirectory_items)}) 

    return translated

if __name__ == "__main__":
    

    opr.print_from("WhisperTranslate", "Starting...")
    path = input("Path: ")
    depth = int(input("Depth: "))
    cleaned_path = fw._clean_path(path)
    directory = fw.get_directory_contents(cleaned_path, depth)        
    translated_directory = translate_files(directory)    
    if fw.save_clean_files(translated_directory):
        opr.print_from("WhisperTranslate", f"SUCCESS: Saving translated directory was successful")
    else:
        opr.print_from("WhisperTranslate", f"FAILED: Saving translated directory was unsuccessful")