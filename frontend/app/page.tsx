'use client';

import { useState, useRef } from 'react';

export default function Home() {
    const [selectedImage, setSelectedImage] = useState<string | null>(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [results, setResults] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    const [systemStatus, setSystemStatus] = useState('Connecting...');
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Check backend on mount
    useState(() => {
        fetch('http://localhost:5000/health')
            .then(() => setSystemStatus('System Ready'))
            .catch(() => setSystemStatus('Offline'));
    });

    const handleFileSelect = (file: File) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            setSelectedImage(e.target?.result as string);
            setResults(null);
            setError(null);
        };
        reader.readAsDataURL(file);
    };

    const analyzeImage = async () => {
        if (!selectedImage) return;
        setIsAnalyzing(true);
        setError(null);

        try {
            const response = await fetch(selectedImage);
            const blob = await response.blob();
            const formData = new FormData();
            formData.append('image', blob, 'image.jpg');

            const apiResponse = await fetch('http://localhost:5000/detect', {
                method: 'POST',
                body: formData,
            });

            if (!apiResponse.ok) throw new Error('Detection failed');
            const data = await apiResponse.json();
            setResults(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <header className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-xl p-6 mb-8">
                    <div className="flex justify-between items-center">
                        <div className="flex items-center gap-4">
                            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg">
                                <span className="text-2xl">👁️</span>
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-gray-800">Third Eye</h1>
                                <p className="text-sm text-gray-500">AI Safety Detection</p>
                            </div>
                        </div>
                        <div className="px-4 py-2 bg-white rounded-full shadow-md">
                            <span className="text-sm font-medium text-gray-700">{systemStatus}</span>
                        </div>
                    </div>
                </header>

                {/* Hero */}
                <div className="text-center mb-12">
                    <h2 className="text-5xl font-bold text-gray-800 mb-4">
                        Detect, analyze, and track
                        <br />
                        <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                            all in one place
                        </span>
                    </h2>
                    <p className="text-xl text-gray-600">AI-powered helmet detection and traffic violation analysis</p>
                </div>

                {/* Main Grid */}
                <div className="grid lg:grid-cols-2 gap-8">
                    {/* Upload Card */}
                    <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl p-8">
                        <h3 className="text-2xl font-bold text-gray-800 mb-6">Upload Image</h3>

                        {!selectedImage ? (
                            <div
                                onClick={() => fileInputRef.current?.click()}
                                className="border-2 border-dashed border-blue-200 rounded-2xl p-12 text-center cursor-pointer hover:border-blue-400 hover:bg-blue-50/50 transition-all"
                            >
                                <input
                                    ref={fileInputRef}
                                    type="file"
                                    accept="image/*"
                                    onChange={(e) => e.target.files && handleFileSelect(e.target.files[0])}
                                    className="hidden"
                                />
                                <div className="w-24 h-24 mx-auto mb-6 rounded-3xl bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center">
                                    <span className="text-4xl">☁️</span>
                                </div>
                                <h3 className="text-xl font-semibold text-gray-800 mb-2">Drop your image here</h3>
                                <p className="text-gray-500 mb-6">or click to browse files</p>
                                <button className="px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-full font-medium shadow-lg">
                                    Choose Image
                                </button>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                <div className="flex justify-between items-center">
                                    <h4 className="text-lg font-semibold text-gray-700">Preview</h4>
                                    <button
                                        onClick={() => setSelectedImage(null)}
                                        className="px-4 py-2 bg-gray-100 rounded-xl text-sm font-medium text-gray-700"
                                    >
                                        New Image
                                    </button>
                                </div>
                                <img src={selectedImage} alt="Preview" className="w-full rounded-2xl" />
                                <button
                                    onClick={analyzeImage}
                                    disabled={isAnalyzing}
                                    className="w-full py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-2xl font-semibold shadow-lg text-lg disabled:opacity-50"
                                >
                                    {isAnalyzing ? 'Analyzing...' : 'Analyze Image'}
                                </button>
                            </div>
                        )}
                    </div>

                    {/* Results Card */}
                    {results ? (
                        <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl p-8">
                            <h3 className="text-2xl font-bold text-gray-800 mb-6">Detection Results</h3>

                            {/* Main Stats Grid */}
                            <div className="grid grid-cols-2 gap-4 mb-6">
                                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-5 border border-blue-100">
                                    <p className="text-sm text-gray-600 mb-1">Total Detections</p>
                                    <p className="text-3xl font-bold text-blue-600">{results.total_detections || 0}</p>
                                </div>
                                <div className="bg-gradient-to-br from-red-50 to-pink-50 rounded-2xl p-5 border border-red-100">
                                    <p className="text-sm text-gray-600 mb-1">Violations</p>
                                    <p className="text-3xl font-bold text-red-600">{results.violations?.total_violations || 0}</p>
                                </div>
                            </div>

                            {/* Additional Metrics */}
                            {results.detections && results.detections.length > 0 && (
                                <div className="grid grid-cols-3 gap-3 mb-6">
                                    <div className="bg-green-50 rounded-xl p-4 border border-green-100">
                                        <p className="text-xs text-gray-600 mb-1">With Helmet</p>
                                        <p className="text-2xl font-bold text-green-600">
                                            {results.detections.filter((d: any) => d.class.toLowerCase().includes('helmet') && !d.class.toLowerCase().includes('without')).length}
                                        </p>
                                    </div>
                                    <div className="bg-orange-50 rounded-xl p-4 border border-orange-100">
                                        <p className="text-xs text-gray-600 mb-1">Without Helmet</p>
                                        <p className="text-2xl font-bold text-orange-600">
                                            {results.detections.filter((d: any) => d.class.toLowerCase().includes('without')).length}
                                        </p>
                                    </div>
                                    <div className="bg-purple-50 rounded-xl p-4 border border-purple-100">
                                        <p className="text-xs text-gray-600 mb-1">Avg Confidence</p>
                                        <p className="text-2xl font-bold text-purple-600">
                                            {Math.round(results.detections.reduce((acc: number, d: any) => acc + parseFloat(d.confidence), 0) / results.detections.length)}%
                                        </p>
                                    </div>
                                </div>
                            )}

                            {/* Annotated Image */}
                            <div>
                                <h4 className="text-sm font-semibold text-gray-700 mb-3">Analyzed Image</h4>
                                <img src={results.annotated_image} alt="Results" className="w-full rounded-2xl shadow-xl" />
                            </div>
                        </div>
                    ) : (
                        <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl p-8">
                            <h3 className="text-2xl font-bold text-gray-800 mb-6">Why Third Eye?</h3>

                            <div className="space-y-4">
                                <div className="flex gap-4 p-4 rounded-2xl bg-blue-50 border border-blue-100">
                                    <div className="text-3xl">🎯</div>
                                    <div>
                                        <h4 className="font-semibold text-gray-800 mb-1">Accurate Detection</h4>
                                        <p className="text-sm text-gray-600">AI-powered helmet detection using advanced computer vision</p>
                                    </div>
                                </div>

                                <div className="flex gap-4 p-4 rounded-2xl bg-indigo-50 border border-indigo-100">
                                    <div className="text-3xl">⚡</div>
                                    <div>
                                        <h4 className="font-semibold text-gray-800 mb-1">Real-time Processing</h4>
                                        <p className="text-sm text-gray-600">Fast analysis with instant results and visualizations</p>
                                    </div>
                                </div>

                                <div className="flex gap-4 p-4 rounded-2xl bg-purple-50 border border-purple-100">
                                    <div className="text-3xl">🛡️</div>
                                    <div>
                                        <h4 className="font-semibold text-gray-800 mb-1">Safety First</h4>
                                        <p className="text-sm text-gray-600">Helping enforce helmet compliance for rider safety</p>
                                    </div>
                                </div>

                                <div className="flex gap-4 p-4 rounded-2xl bg-green-50 border border-green-100">
                                    <div className="text-3xl">📊</div>
                                    <div>
                                        <h4 className="font-semibold text-gray-800 mb-1">Detailed Analytics</h4>
                                        <p className="text-sm text-gray-600">Comprehensive violation reports and statistics</p>
                                    </div>
                                </div>

                                <div className="flex gap-4 p-4 rounded-2xl bg-orange-50 border border-orange-100">
                                    <div className="text-3xl">🚀</div>
                                    <div>
                                        <h4 className="font-semibold text-gray-800 mb-1">Easy to Use</h4>
                                        <p className="text-sm text-gray-600">Simply upload an image and get instant detection results</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Loading */}
                {isAnalyzing && (
                    <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
                        <div className="bg-white rounded-3xl p-10 max-w-md">
                            <div className="flex justify-center mb-6">
                                <div className="w-20 h-20 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                            </div>
                            <h3 className="text-2xl font-bold text-center mb-2">Analyzing...</h3>
                            <p className="text-gray-600 text-center">Processing your image</p>
                        </div>
                    </div>
                )}

                {/* Error */}
                {error && (
                    <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
                        <div className="bg-white rounded-3xl p-10 max-w-md text-center">
                            <div className="text-6xl mb-4">⚠️</div>
                            <h3 className="text-2xl font-bold mb-2">Error</h3>
                            <p className="text-gray-600 mb-8">{error}</p>
                            <button
                                onClick={() => setError(null)}
                                className="px-8 py-3 bg-red-500 text-white rounded-full font-medium"
                            >
                                Dismiss
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
