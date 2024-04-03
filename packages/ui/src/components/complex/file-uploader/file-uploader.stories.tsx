import React from "react";
import type {Meta, StoryObj} from "@storybook/react";
import {FileUploader} from "@ui/components";

const meta: Meta<typeof FileUploader> = {
  component: FileUploader,
  argTypes: {
    title: {control: "text"},
    size: {control: {type: 'radio'}, options: ['small', 'medium', 'large']},
  },
};

export default meta;

type Story = StoryObj<typeof FileUploader>;

export const Primary: Story = {
  render: (args) => <FileUploader className="ui-max-w-1/2" {...args} />,
  args: {
    title: "Upload a file",
    size: "medium",
  },
  name: "File Upload"
}

