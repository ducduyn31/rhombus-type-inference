import type {ComponentProps} from "react";
import React from "react";
import type {Meta, StoryObj} from "@storybook/react";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "./card";
import {Label} from "./label";
import {Input} from "./input";
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from "./select";

interface DemoCardMeta extends ComponentProps<typeof Card>{
  description: string,
  placeholder: string,
}

const meta: Meta<DemoCardMeta> = {
  component: Card,
  argTypes: {
    title: {control: "text"},
    description: {control: "text"},
    placeholder: {control: "text"},
  },
};

export default meta;

type Story = StoryObj<DemoCardMeta>;

/*
 *👇 Render functions are a framework specific feature to allow you control on how the component renders.
 * See https://storybook.js.org/docs/react/api/csf
 * to learn how to use render functions.
 */
export const Primary: Story = {
  render: (props) => (
    <Card className="ui-w-[350px]"
    >
      <CardHeader>
        <CardTitle>{props.title}</CardTitle>
        <CardDescription>{props.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="name">Name</Label>
              <Input id="name" placeholder={props.placeholder}/>
            </div>
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="framework">Framework</Label>
              <Select>
                <SelectTrigger id="framework">
                  <SelectValue placeholder="Select"/>
                </SelectTrigger>
                <SelectContent position="popper">
                  <SelectItem value="next">Next.js</SelectItem>
                  <SelectItem value="sveltekit">SvelteKit</SelectItem>
                  <SelectItem value="astro">Astro</SelectItem>
                  <SelectItem value="nuxt">Nuxt.js</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </form>
      </CardContent>
    </Card>
  ),
  name: "Card",
  args: {
    children: "Hello",
    title: "Create Project",
    description: "Deploy your new project in one-click.",
    placeholder: "Name of your project",
  },
};