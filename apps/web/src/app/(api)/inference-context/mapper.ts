export const npTypesToHumanReadable = {
  'int8': "Integers (8-bit)",
  'int16': "Integers (16-bit)",
  'int32': "Integers (32-bit)",
  'int64': "Integers (64-bit)",
  'uint8': "Unsigned Integers (8-bit)",
  'uint16': "Unsigned Integers (16-bit)",
  'uint32': "Unsigned Integers (32-bit)",
  'uint64': "Unsigned Integers (64-bit)",
  'float16': "Floating Point Numbers (16-bit)",
  'float32': "Floating Point Numbers (32-bit)",
  'float64': "Floating Point Numbers (64-bit)",
  'bool': "Boolean",
  'object': "Text",
  'category': "Categorical",
  'datetime64': "Date/Time",
  'datetime64[ns]': "Date/Time",
  'timedelta64': "Time Delta",
} as const;

export const convertNpTypeToHumanReadable = (types: Record<string, string>): Record<string, string> => {
  return Object.fromEntries(
    Object.entries(types).map(([key, value]) =>{
      if (value in npTypesToHumanReadable) {
        return [key, npTypesToHumanReadable[value as keyof typeof npTypesToHumanReadable]];
      }
      return [key, value];
    })
  );
}