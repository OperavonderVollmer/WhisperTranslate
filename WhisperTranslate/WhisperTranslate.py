from OperaPowerRelay import opr
from FileWhisperer import FileWhisperer as fw
from deep_translator import GoogleTranslator
import traceback
import os
from pathlib import Path

"""
    WhisperTranslate is a script that works in conjunction with FileWhisperer to translate the 
    filename and metadata of files and directories
"""
TRANSLATOR = GoogleTranslator(source='auto', target='en')
TRANSLATE_CACHE: dict[str, str] = {}

def get_version() -> str:
    return "1.0"

def change_translator(source: str, target: str):
    global TRANSLATOR
    TRANSLATOR = GoogleTranslator(source=source, target=target)


def translate_with_metadata(file: fw.CleanFile) -> fw.CleanFile | None:
    
    try:
        translated_file_name = pure_translate(file.Name)
        if translated_file_name:
            file.Name = translated_file_name


# translate relative file path here
        """directory_path = os.path.dirname(file.Path)
        base_parent_folder = os.path.basename(directory_path)

        translated_parent_folder = pure_translate(base_parent_folder)
        if translated_parent_folder:            
            path = os.path.join(os.path.dirname(directory_path), translated_parent_folder, translated_file_name)
            opr.print_from("WhisperTranslate - Translate with Metadata", f"SUCCESS: Translated original file path from '{file._original_path}' to new file path '{path}'")
            file.Path = path"""
        

        path_list = list(Path(file.RelativePath).parts)
        new_path_list = []
        for i in range(len(path_list)):
            new_path_list.append(pure_translate(path_list[i]))
        
        if new_path_list:
            path = os.path.join(file.ProvidedPath, Path(*new_path_list) )
            opr.print_from("WhisperTranslate - Translate with Metadata", f"SUCCESS: Translated original file path from '{file._original_path}' to new file path '{path}'")
            file.Path = path

        if any(file.Path.endswith(f) for f in fw.AUDIO_FORMATS):
            translated_audio_title = pure_translate(file.Metadata_dict["TITLE"]) 
            if translated_audio_title:
                file.Metadata_dict["TITLE"] = translated_audio_title
    # include logic to deal with other file formats here
        else:
            opr.print_from("WhisperTranslate - Translate with Metadata", f"SKIPPED: {file.Name}'s file format is not supported")
                
        return file
    except Exception:
        error_message = traceback.format_exc()
        opr.print_from("WhisperTranslate - Translate with Metadata", f"FAILED: Unexpected Error while translating {file.Name}: {error_message}")
        return None

def pure_translate(word: str) -> str | None:
    global TRANSLATOR

    if word in TRANSLATE_CACHE.keys():
        return TRANSLATE_CACHE[word]

    translate_word = TRANSLATOR.translate(word)
    if not translate_word:
        raise Exception
    
    TRANSLATE_CACHE[word] = translate_word

    opr.print_from("WhisperTranslate - Pure Translate", f"SUCCESS: Translated {word} to {translate_word}")

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

"""def translate_files(files: list[fw.CleanFile | dict[str, list]], parent_path: str = "") -> list[fw.CleanFile | dict[str, list]]:
    translated: list[fw.CleanFile | dict[str, list]] = []

    for f in files:
        if isinstance(f, fw.CleanFile):
            _ = translate_with_metadata(f)
            if _:
                if parent_path:
                    _.Path = os.path.join(parent_path, _.Name)
                translated.append(_)
        elif isinstance(f, dict):
            subdirectory_name, subdirectory_items = next(iter(f.items()))

            translated_subdir_name = pure_translate(subdirectory_name) or subdirectory_name
            translated_subdir_path = os.path.join(parent_path, translated_subdir_name)

            translated.append({
                translated_subdir_name: translate_files(subdirectory_items, translated_subdir_path)
            })

    return translated"""

    
if __name__ == "__main__":
    
    os.system('cls')

    opr.print_from("WhisperTranslate", "Starting...")
    path = input("[WhisperTranslate] Please enter a path (drag and drop): ")
    depth = int(input("[WhisperTranslate] Please enter the depth: "))
    cleaned_path = fw._clean_path(path)
    directory = fw.get_directory_contents(cleaned_path, depth)
    opr.print_from("WhisperTranslate", "Successfully retrieved directory contents")

    _ = input("[WhisperTranslate] Would you like to see the directory contents? (y/n): ") 
    if _ == "y":
        fw.display_files(directory)
    
    _ = input("[WhisperTranslate] Continue with the translation? (y/n): ")
    if _ == "y":

        translated_directory = translate_files(directory)    
        if fw.save_clean_files(translated_directory):
            opr.print_from("WhisperTranslate", f"SUCCESS: Saving translated directory was successful")
        else:
            opr.print_from("WhisperTranslate", f"FAILED: Saving translated directory was unsuccessful")










