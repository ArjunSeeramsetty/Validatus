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
          
          // Validate JSON structure
          if (!json.detailed_analysis) {
            console.warn('WARNING: detailed_analysis section is missing from parsed JSON');
            console.warn('Available top-level keys:', Object.keys(json));
            
            // Check if the JSON was truncated during parsing
            const jsonString = e.target?.result as string;
            if (jsonString.includes('"detailed_analysis"')) {
              console.warn('"detailed_analysis" string found in raw JSON but not in parsed object - possible parsing issue');
              
              // Find the position of detailed_analysis in the raw string
              const detailedAnalysisIndex = jsonString.indexOf('"detailed_analysis"');
              console.log('Position of "detailed_analysis" in raw JSON:', detailedAnalysisIndex);
              
              // Show the content around detailed_analysis
              const start = Math.max(0, detailedAnalysisIndex - 100);
              const end = Math.min(jsonString.length, detailedAnalysisIndex + 500);
              console.log('Content around "detailed_analysis":', jsonString.substring(start, end));
              
              // Check if the JSON is properly closed
              const openBraces = (jsonString.match(/\{/g) || []).length;
              const closeBraces = (jsonString.match(/\}/g) || []).length;
              console.log('Brace count - Open:', openBraces, 'Close:', closeBraces, 'Balance:', openBraces - closeBraces);
              
              // Try to manually extract detailed_analysis section
              console.log('Attempting manual extraction of detailed_analysis...');
              const detailedAnalysisStart = jsonString.indexOf('"detailed_analysis"');
              if (detailedAnalysisStart !== -1) {
                // Find the opening brace after "detailed_analysis":
                const braceStart = jsonString.indexOf('{', detailedAnalysisStart);
                if (braceStart !== -1) {
                  // Try to find the matching closing brace
                  let braceCount = 0;
                  let braceEnd = -1;
                  for (let i = braceStart; i < jsonString.length; i++) {
                    if (jsonString[i] === '{') braceCount++;
                    if (jsonString[i] === '}') {
                      braceCount--;
                      if (braceCount === 0) {
                        braceEnd = i;
                        break;
                      }
                    }
                  }
                  
                  if (braceEnd !== -1) {
                    const detailedAnalysisSection = jsonString.substring(detailedAnalysisStart, braceEnd + 1);
                    console.log('Manually extracted detailed_analysis section:', detailedAnalysisSection.substring(0, 500) + '...');
                    
                    // Try to parse just this section
                    try {
                      const extractedJson = JSON.parse('{' + detailedAnalysisSection + '}');
                      console.log('SUCCESS: Manually extracted detailed_analysis parses correctly:', Object.keys(extractedJson.detailed_analysis || {}));
                      
                      // If manual extraction works, try to merge it with the main JSON
                      if (extractedJson.detailed_analysis) {
                        json.detailed_analysis = extractedJson.detailed_analysis;
                        console.log('MERGED: Added detailed_analysis to main JSON object');
                      }
                    } catch (extractError) {
                      console.log('FAILED: Manually extracted section still has parsing errors:', extractError);
                    }
                  } else {
                    console.log('Could not find matching closing brace for detailed_analysis');
                  }
                }
              }
            } else {
              console.warn('"detailed_analysis" string not found in raw JSON');
            }
          } else {
            console.log('SUCCESS: detailed_analysis section found with keys:', Object.keys(json.detailed_analysis));
          }
          
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

