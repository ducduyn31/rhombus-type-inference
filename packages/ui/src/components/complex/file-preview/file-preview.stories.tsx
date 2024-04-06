import type {ComponentProps} from "react";
import React from "react";
import type {Meta, StoryObj} from "@storybook/react";
import {FilePreview} from "@ui/components";

interface FilePreviewMeta extends ComponentProps<typeof FilePreview> {
  filename: string;
  size: number;
  type: "csv" | "xlsx" | "xls";
}

const meta: Meta<FilePreviewMeta> = {
  component: FilePreview,
  argTypes: {
    filename: {
      control: {
        type: "text",
      },
    },
    size: {
      control: {
        type: "number",
      },
    },
    type: {control: {type: 'radio'}, options: ['csv', 'xlsx', 'xls']},
    uploadProgress: {
      control: {
        type: "range",
        min: 0,
        max: 100,
        step: 1,
      },
    }
  },
};

export default meta;

type Story = StoryObj<FilePreviewMeta>;

export const Primary: Story = {
  render: (props) => {
    const {
      filename,
      type,
      file,
      size,
      ...rest
    } = props;
    const mimeTypes = {
      csv: "text/csv",
      xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      xls: "application/vnd.ms-excel",
    };

    let state: "uploaded" | "uploading" | "none" = "none"
    if (props.uploadProgress && props.uploadProgress === 100) {
      state = "uploaded";
    } else if (props.uploadProgress && props.uploadProgress > 0) {
      state = "uploading";
    }

    const fakeFile = file || new File(new Array<BlobPart>(size).fill("0"), filename, {type: mimeTypes[type]});
    return <FilePreview file={fakeFile} state={state} {...rest} />;
  },
  args: {
    filename: "file.csv",
    size: 1024,
    type: "csv",
    uploadProgress: 0,
  },
  name: "File Uploaded Item"
}

