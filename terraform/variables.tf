variable "project_id" {
  description = "Your GCP Project ID"
  type        = string
}

variable "region" {
  description = "Region for GCP resources"
  default     = "us-central1"
  type        = string
}