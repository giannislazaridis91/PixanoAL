/**
@copyright CEA-LIST/DIASI/SIALV/LVA (2023)
@author CEA-LIST/DIASI/SIALV/LVA <pixano@cea.fr>
@license CECILL-C

This software is a collaborative computer program whose purpose is to
generate and explore labeled data for computer vision applications.
This software is governed by the CeCILL-C license under French law and
abiding by the rules of distribution of free software. You can use, 
modify and/ or redistribute the software under the terms of the CeCILL-C
license as circulated by CEA, CNRS and INRIA at the following URL

http://www.cecill.info
*/

import type { Meta, StoryObj } from "@storybook/svelte";
import DataPanel from "../../../../../apps/annotator/src/lib/DataPanel.svelte";

const meta = {
  title: "Applications/Annotator/DataPanel",
  component: DataPanel,
  tags: ["autodocs"],
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta<DataPanel>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Base: Story = {
  args: {
    annotations: [
      { 
        category_name: "Dog", 
        viewId: "view1",
        items: [
          { id: "0x123", type: "mask", label: "dog-0", visible: true, opacity: 1.0 },
          { id: "0x354", type: "mask", label: "dog-1", visible: true, opacity: 1.0 },
        ],
        visible: true,
      },
      { 
        category_name: "Cat", 
        viewId: "view1",
        items: [
          { id: "0x237", type: "mask", label: "cat-0", visible: true, opacity: 1.0 },
        ],
        visible: true,
      },
      { 
        category_name: "Cat", 
        viewId: "view2",
        items: [
          { id: "0x487", type: "mask", label: "cat-0", visible: true, opacity: 1.0 },
        ],
        visible: true,
      },
    ],
    dbImages: [
      "img-01.jpg",
      "img-02.jpg",
      "img-03.jpg",
      "img-04.jpg",
      "img-05.jpg",
      "img-06.jpg",
      "img-07.jpg",
      "img-08.jpg",
    ],
  },
};
