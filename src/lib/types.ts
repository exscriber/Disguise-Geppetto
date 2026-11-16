// Created by Nick N. Zinovenko
// This code is freely distributable under the terms of the [MIT license]

export interface LayerSettings {
  isEnabled: boolean
  numLayers: number | null
  dmxAddress: string
  groupBy: number | null
}

export interface Personality {
  iver?: number
  ver: number
  dmx: number
}
