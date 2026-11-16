// Created by Nick N. Zinovenko
// This code is freely distributable under the terms of the [MIT license]

export function sleep(ms: number) {
  return new Promise<void>((resolve) => setTimeout(resolve, ms))
}

export function sleep_dev(ms: number) {
  if (import.meta.env.PROD) return Promise.resolve()
  return new Promise<void>((resolve) => setTimeout(resolve, ms))
}

export function range(start: number, stop: number, step: number) {
  return Array.from({ length: Math.ceil((stop - start) / step) }, (_, i) => start + i * step)
}
