import type {FC, PropsWithChildren, Ref} from "react";
import {createContext, useContext, useState} from "react";

interface FileUploaderContextType {
  file: File | null;
  setFile: (file: File) => void;
  triggerFileSelect: () => void;
}

const FileUploaderContext = createContext<FileUploaderContextType>({
  file: null,
  setFile: () => {
  },
  triggerFileSelect: () => {
  }
})

interface FileUploaderProviderProps extends PropsWithChildren {
  inputRef?: Ref<HTMLInputElement>;
}

const FileUploaderProvider: FC<FileUploaderProviderProps> = ({children, inputRef}) => {
  const [file, setFile] = useState<File | null>(null);

  const triggerFileSelect = (): void => {
    if (inputRef && "current" in inputRef && inputRef.current) {
      inputRef.current.click();
    }
  }

  return (
    <FileUploaderContext.Provider value={{file, setFile, triggerFileSelect}}>
      {children}
    </FileUploaderContext.Provider>
  )

}

const useFileUploader = (): FileUploaderContextType =>
  useContext(FileUploaderContext);

export {FileUploaderProvider, useFileUploader};