"use client"

import type React from "react"
import { useRef, useState } from "react"
import { Upload, FileVideo, AlertCircle, CheckCircle2 } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { api } from '@/lib/api'

interface VideoUploaderProps {
  onFileSelect: (file: File) => void
  onStatusChange: (status: "idle" | "uploading" | "orchestrating" | "completed" | "error") => void
  onCampaignCreated?: (campaign: any) => void  // Add this prop to pass campaign data
}

export function VideoUploader({ onFileSelect, onStatusChange, onCampaignCreated }: VideoUploaderProps) {
  const [file, setFile] = useState<File | null>(null)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [isUploading, setIsUploading] = useState(false)
  const [useManualTranscript, setUseManualTranscript] = useState(false)
  const [manualTranscript, setManualTranscript] = useState("")
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const SUPPORTED_FORMATS = ["video/mp4", "video/quicktime", "video/webm"]
  const MAX_FILE_SIZE = 500 * 1024 * 1024

  const validateFile = (selectedFile: File): boolean => {
    if (!SUPPORTED_FORMATS.includes(selectedFile.type)) {
      setError("Please upload an MP4, MOV, or WebM file")
      return false
    }
    if (selectedFile.size > MAX_FILE_SIZE) {
      setError("File size must be under 500MB")
      return false
    }
    setError(null)
    return true
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile && validateFile(selectedFile)) {
      setFile(selectedFile)
      // Don't auto-upload, wait for submit button
    }
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const droppedFile = e.dataTransfer.files?.[0]
    if (droppedFile && validateFile(droppedFile)) {
      setFile(droppedFile)
      // Don't auto-upload, wait for submit button
    }
  }

  const processVideo = async () => {
    if (!file && !manualTranscript) {
      setError("Please upload a video or provide a transcript")
      return
    }

    setIsUploading(true)
    setError(null)
    onStatusChange("uploading")

    try {
      let campaignResult

      if (file) {
        // Upload video and get transcript
        console.log("Uploading video:", file.name)
        setUploadProgress(30)
        const uploadResult = await api.uploadVideo(file)
        console.log("Upload complete, transcript:", uploadResult.transcript)
        
        setUploadProgress(60)
        onStatusChange("orchestrating")
        
        // Create campaign from video transcript
        campaignResult = await api.createCampaign(
          uploadResult.transcript,
          { title: file.name }
        )
      } else if (manualTranscript) {
        // Create campaign from manual transcript
        console.log("Using manual transcript")
        onStatusChange("orchestrating")
        campaignResult = await api.createCampaignFromTranscript(
          manualTranscript,
          "Manual Transcript"
        )
      }

      setUploadProgress(100)
      
      if (campaignResult) {
        console.log("Campaign created successfully:", campaignResult)
        
        // Pass campaign data to parent component if handler provided
        if (onCampaignCreated) {
          onCampaignCreated(campaignResult)
        }
        
        // Show success message
        onStatusChange("completed")
        
        // You can also display the campaign data here
        alert(`Campaign created! ID: ${campaignResult.id}`)
      }
      
    } catch (error) {
      console.error("Error processing:", error)
      setError(error instanceof Error ? error.message : "Failed to process video")
      onStatusChange("error")
    } finally {
      setIsUploading(false)
      setUploadProgress(0)
    }
  }

  const handleSubmit = () => {
    if (!file && !manualTranscript) {
      setError("Please upload a video or provide a transcript")
      return
    }
    if (!file && useManualTranscript && !manualTranscript.trim()) {
      setError("Please enter a transcript")
      return
    }
    if (file) {
      onFileSelect(file)
    }
    processVideo()
  }

  return (
    <Card className="border border-border shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileVideo className="w-5 h-5 text-primary" />
          Upload Video Content
        </CardTitle>
        <CardDescription>
          Drag and drop your video file (MP4, MOV, WebM up to 500MB) or provide a transcript manually
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {error && (
          <Alert variant="destructive" role="alert">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {file && !isUploading && (
          <Alert className="border-green-500/50 bg-green-500/5">
            <CheckCircle2 className="h-4 w-4 text-green-600" />
            <AlertDescription className="text-green-700 dark:text-green-400">File ready: {file.name}</AlertDescription>
          </Alert>
        )}

        {/* Drag & Drop Zone */}
        <div
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          className="border-2 border-dashed border-border rounded-lg p-6 sm:p-8 text-center hover:border-primary/50 hover:bg-primary/5 transition-colors cursor-pointer focus-within:ring-2 focus-within:ring-ring"
          onClick={() => fileInputRef.current?.click()}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              fileInputRef.current?.click()
            }
          }}
          role="button"
          tabIndex={0}
          aria-label="Upload video file"
        >
          <Upload className="w-8 sm:w-10 h-8 sm:h-10 mx-auto mb-3 text-muted-foreground" />
          <h3 className="font-semibold text-foreground mb-1">Drop your video here</h3>
          <p className="text-sm text-muted-foreground">or click to browse files</p>
          <Input
            ref={fileInputRef}
            type="file"
            accept="video/*"
            onChange={handleFileChange}
            className="hidden"
            aria-label="Video file input"
          />
        </div>

        {/* Upload Progress */}
        {isUploading && (
          <div
            className="space-y-2"
            role="progressbar"
            aria-valuenow={uploadProgress}
            aria-valuemin={0}
            aria-valuemax={100}
          >
            <div className="flex justify-between text-sm">
              <span className="text-foreground">
                {uploadProgress < 50 ? "Uploading..." : "Creating campaign..."}
              </span>
              <span className="text-muted-foreground">{uploadProgress}%</span>
            </div>
            <div className="w-full bg-border rounded-full h-2 overflow-hidden">
              <div className="bg-primary h-full transition-all duration-300" style={{ width: `${uploadProgress}%` }} />
            </div>
          </div>
        )}

        {/* Manual Transcript Option */}
        <div className="border-t border-border pt-6">
          <div className="flex items-center gap-2 mb-4">
            <input
              type="checkbox"
              id="manual-transcript"
              checked={useManualTranscript}
              onChange={(e) => setUseManualTranscript(e.target.checked)}
              className="w-4 h-4 rounded border-border"
            />
            <label htmlFor="manual-transcript" className="text-sm font-medium text-foreground cursor-pointer">
              Use manual transcript instead
            </label>
          </div>

          {useManualTranscript && (
            <Textarea
              value={manualTranscript}
              onChange={(e) => setManualTranscript(e.target.value)}
              placeholder="Paste your video transcript here..."
              className="min-h-32 text-foreground bg-card border-border"
            />
          )}
        </div>

        {/* Submit Button */}
        <Button
          onClick={handleSubmit}
          disabled={isUploading || (!file && !manualTranscript.trim())}
          className="w-full bg-primary hover:bg-primary/90 text-primary-foreground"
          size="lg"
        >
          {isUploading ? "Processing..." : "Start Campaign Generation"}
        </Button>
      </CardContent>
    </Card>
  )
}