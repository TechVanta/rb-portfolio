import FileUploader from "../components/FileUploader";

export default function UploadPage() {
  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Upload Statement</h1>
        <p className="text-sm text-gray-500 mt-1">
          Upload your credit card or bank statement to automatically extract and categorize transactions.
        </p>
      </div>

      <FileUploader />

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-medium text-blue-800 mb-2">Supported Formats</h3>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• <strong>CSV files</strong> — Most bank export formats with Date, Description, and Amount columns</li>
          <li>• <strong>PDF statements</strong> — Structured text-based PDFs (not scanned images)</li>
        </ul>
      </div>
    </div>
  );
}
