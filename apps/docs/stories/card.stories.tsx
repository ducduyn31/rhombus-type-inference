import React from "react";
import type {Meta, StoryObj} from "@storybook/react";
import {Card} from "@repo/ui/components";

const meta: Meta<typeof Card> = {
  component: Card,
  argTypes: {
    title: {control: "text"},
  },
};

export default meta;

type Story = StoryObj<typeof Card>;

/*
 *👇 Render functions are a framework specific feature to allow you control on how the component renders.
 * See https://storybook.js.org/docs/react/api/csf
 * to learn how to use render functions.
 */
export const Primary: Story = {
  render: (props) => (
    <Card
      {...props}
    >
      Hello
    </Card>
  ),
  name: "Card",
  args: {
    children: "Hello",
    title: "World",
  },
};