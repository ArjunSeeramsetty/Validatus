import React from 'react';

interface HomePageProps {
  onStartNewAnalysis: () => void;
  onLoadAnalysis: (data: any) => void;
}

const HomePage: React.FC<HomePageProps> = ({ onStartNewAnalysis, onLoadAnalysis }) => {
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const json = JSON.parse(e.target?.result as string);
          onLoadAnalysis(json);
        } catch (error) {
          console.error("Failed to parse JSON file", error);
          alert("Invalid JSON file. Please upload a valid analysis report.");
        }
      };
      reader.readAsText(file);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-8">
      <div className="w-full max-w-2xl text-center">
        <h1 className="text-5xl font-bold text-gray-800 mb-4">Validatus</h1>
        <p className="text-xl text-gray-600 mb-12">
          Your AI-powered strategic analysis platform.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Start New Analysis Card */}
          <div
            className="bg-white p-8 rounded-lg shadow-md hover:shadow-xl transition-shadow cursor-pointer border border-gray-200"
            onClick={onStartNewAnalysis}
          >
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">Start New Analysis</h2>
            <p className="text-gray-500">
              Provide a business idea and target audience to generate a new, comprehensive strategic report.
            </p>
          </div>

          {/* Load Previous Analysis Card */}
          <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-xl transition-shadow border border-gray-200">
             <label htmlFor="file-upload" className="cursor-pointer block w-full h-full">
                <h2 className="text-2xl font-semibold text-gray-700 mb-4">Visualize Report</h2>
                <p className="text-gray-500">
                Upload a JSON report to explore the interactive analysis dashboard.
                </p>
             </label>
            <input
              id="file-upload"
              type="file"
              accept=".json"
              className="hidden"
              onChange={handleFileChange}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

