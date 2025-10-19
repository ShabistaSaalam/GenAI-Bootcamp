"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"

export default function VocabImporter() {
  const [category, setCategory] = useState("")
  const [loading, setLoading] = useState(false)
  const [jsonText, setJsonText] = useState("")

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!category.trim()) {
      alert("Please enter a thematic category.") // simple alert instead of toast
      return
    }
    setLoading(true)
    setJsonText("")
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category }),
      })
      if (!res.ok) {
        const msg = await res.text()
        throw new Error(msg || "Failed to generate.")
      }
      const data = await res.json()
      const pretty = data?.json ? JSON.stringify(data.json, null, 2) : (data?.raw ?? "")
      setJsonText(pretty)
    } catch (err: any) {
      alert(err?.message ?? "Something went wrong.") // simple alert for error
    } finally {
      setLoading(false)
    }
  }

  async function onCopy() {
    if (!jsonText) return
    await navigator.clipboard.writeText(jsonText)
    alert("JSON copied to clipboard.") // simple alert on copy
  }

  return (
    <section className="space-y-6">
      <form onSubmit={onSubmit} className="grid gap-4">
        <div className="grid gap-2">
          <label htmlFor="category" className="text-sm font-medium">
            Thematic category
          </label>
          <Input
            id="category"
            placeholder="e.g., Greetings, Food, Travel essentials"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          />
        </div>

        <div className="flex items-center gap-3">
          <Button type="submit" disabled={loading}>
            {loading ? "Generating…" : "Generate JSON"}
          </Button>
          <Button type="button" variant="secondary" onClick={onCopy} disabled={!jsonText}>
            Copy JSON
          </Button>
        </div>
      </form>

      <div className="grid gap-2">
        <label htmlFor="output" className="text-sm font-medium">
          Output (read-only, copyable)
        </label>
        <Textarea
          id="output"
          className="min-h-64 font-mono text-sm"
          value={jsonText}
          readOnly
          placeholder="Generated JSON will appear here…"
        />
      </div>
    </section>
  )
}
