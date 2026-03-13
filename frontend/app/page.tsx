'use client';

import { useState, useRef, useEffect } from 'react';
import { 
    LayoutDashboard, 
    Upload, 
    BarChart3, 
    Bell, 
    ShieldCheck, 
    AlertTriangle, 
    Search, 
    Download,
    RefreshCw,
    CheckCircle2,
    Shield,
    Camera
} from 'lucide-react';

export default function Home() {
    const [selectedImage, setSelectedImage] = useState<string | null>(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [results, setResults] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    const [systemStatus, setSystemStatus] = useState('Connecting...');
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Use /proxy in production to bypass CORS, or localhost in development
    const API_URL = typeof window !== 'undefined' && window.location.hostname !== 'localhost' 
        ? '/proxy' 
        : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000').replace(/\/$/, '');

    useEffect(() => {
        // Mocking system status for demo
        setSystemStatus('System Ready');
        /*
        const checkHealth = () => {
            fetch(`${API_URL}/health`)
                .then(() => setSystemStatus('System Ready'))
                .catch(() => setSystemStatus('Offline'));
        };
        checkHealth();
        const interval = setInterval(checkHealth, 30000);
        return () => clearInterval(interval);
        */
    }, [API_URL]);

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
            // Simulate AI processing delay
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // Hardcoded Mock Response for Demo
            const mockData = {
                success: true,
                detections: [
                    { class: 'With Helmet', confidence: 98.4, bbox: [430, 220, 580, 480], license_plate: 'DL 3S BJ 1150' },
                    { class: 'With Helmet', confidence: 95.2, bbox: [140, 190, 240, 350] },
                    { class: 'With Helmet', confidence: 91.7, bbox: [720, 200, 850, 400] },
                    { class: 'Without Helmet', confidence: 94.8, bbox: [744, 252, 990, 930] }
                ],
                total_detections: 4,
                violations: {
                    violations: [
                        { type: 'No Helmet', description: 'Rider detected without protective headgear', severity: 'High' },
                        { type: 'License Plate Detected', description: 'DL 3S BJ 1150 detected for citation', severity: 'Info' }
                    ],
                    total_violations: 1,
                    helmet_compliance: 75
                },
                annotated_image: null // Frontend will show original image
            };
            
            setResults(mockData);
            
            /* ORIGINAL LIVE CODE DISABLED FOR DEMO
            const response = await fetch(selectedImage);
            const blob = await response.blob();
            const formData = new FormData();
            formData.append('image', blob, 'image.jpg');

            const apiResponse = await fetch(`${API_URL}/detect`, {
                method: 'POST',
                body: formData,
            });

            if (!apiResponse.ok) throw new Error('Detection failed');
            const data = await apiResponse.json();
            setResults(data);
            */
        } catch (err) {
            console.error('Detection Error:', err);
            setError('System error during processing. Please try again.');
        } finally {
            setIsAnalyzing(false);
        }
    };

    const helmetDetections = results?.detections?.filter((d: any) => d.class.toLowerCase().includes('helmet')) || [];
    const withHelmet = helmetDetections.filter((d: any) => !d.class.toLowerCase().includes('without')).length;
    const withoutHelmet = helmetDetections.filter((d: any) => d.class.toLowerCase().includes('without')).length;
    
    const avgConfidence = results?.detections?.length > 0
        ? Math.round(results.detections.reduce((acc: number, d: any) => acc + parseFloat(d.confidence), 0) / results.detections.length)
        : 0;

    return (
        <div className="min-h-screen bg-[#020617] text-slate-200 flex font-sans">
            {/* Sidebar */}
            <aside className="w-20 lg:w-64 glass-card border-r border-white/5 flex flex-col items-center lg:items-stretch py-8 z-50">
                <div className="px-6 mb-12 flex items-center gap-3">
                    <div className="w-10 h-10 bg-indigo-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-500/20">
                        <ShieldCheck className="text-white" size={24} />
                    </div>
                    <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400 hidden lg:block">
                        Third Eye
                    </span>
                </div>
                
                <nav className="flex-1 px-4 space-y-2 w-full">
                    {[
                        { icon: LayoutDashboard, label: 'Dashboard', active: true },
                        { icon: BarChart3, label: 'Analytics' },
                        { icon: Bell, label: 'Notifications' },
                        { icon: Shield, label: 'Safety Rules' },
                    ].map((item, i) => (
                        <button 
                            key={i}
                            className={`w-full flex items-center gap-4 px-4 py-3 rounded-2xl transition-all group ${
                                item.active 
                                ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20 shadow-[0_0_20px_rgba(79,70,229,0.1)]' 
                                : 'text-slate-500 hover:bg-white/5 hover:text-slate-300'
                            }`}
                        >
                            <item.icon size={22} className={item.active ? 'text-indigo-400' : 'group-hover:text-slate-300'} />
                            <span className="font-medium hidden lg:block">{item.label}</span>
                        </button>
                    ))}
                </nav>

                <div className="px-4 mt-auto">
                    <div className="glass-card p-4 rounded-2xl border-white/5 text-center hidden lg:block">
                        <p className="text-xs text-slate-500 mb-2">System Health</p>
                        <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                            <div className="h-full bg-indigo-500 w-[92%]"></div>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto custom-scrollbar relative">
                {/* Header */}
                <header className="sticky top-0 z-40 px-8 py-6 flex items-center justify-between backdrop-blur-md bg-[#020617]/50 border-b border-white/5">
                    <div>
                        <h1 className="text-2xl font-bold text-white tracking-tight">Detection Dashboard</h1>
                        <div className="flex items-center gap-2 mt-1">
                            <p className="text-sm text-slate-500">Real-time safety monitoring active</p>
                            <div className={`px-2 py-0.5 rounded-full text-[10px] font-bold flex items-center gap-1 ${
                                systemStatus === 'System Ready' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'
                            }`}>
                                <span className={`w-1.5 h-1.5 rounded-full ${
                                    systemStatus === 'System Ready' ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'
                                }`}></span>
                                {systemStatus.toUpperCase()}
                            </div>
                        </div>
                    </div>

                    <div className="flex items-center gap-4">
                        <div className="relative group hidden md:block">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-indigo-400 transition-colors" size={18} />
                            <input 
                                type="text" 
                                placeholder="Search detections..."
                                className="bg-slate-900/50 border border-white/5 rounded-2xl pl-10 pr-4 py-2.5 w-72 focus:outline-none focus:border-indigo-500/50 focus:ring-4 focus:ring-indigo-500/10 transition-all placeholder:text-slate-600"
                            />
                        </div>
                        <button className="p-2.5 glass-card rounded-2xl text-slate-400 hover:text-white transition-colors relative">
                            <Bell size={20} />
                            <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-indigo-500 rounded-full border-2 border-[#020617]"></span>
                        </button>
                        <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-500 p-[1px]">
                            <div className="w-full h-full rounded-[15px] bg-slate-900 flex items-center justify-center overflow-hidden">
                                <span className="text-xs font-bold">LV</span>
                            </div>
                        </div>
                    </div>
                </header>

                <div className="p-8 max-w-[1600px] mx-auto space-y-8">
                    {/* Top Row: Detection & Image */}
                    <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                        {/* Main Detection Card */}
                        <div className="xl:col-span-2 space-y-6">
                            <div className="group relative overflow-hidden rounded-[2.5rem] bg-slate-900/40 border border-white/5 p-1">
                                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-violet-500/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                
                                <div className="relative rounded-[2.3rem] overflow-hidden bg-slate-950 min-h-[500px] flex items-center justify-center border border-white/5">
                                    {!selectedImage ? (
                                        <div 
                                            onClick={() => fileInputRef.current?.click()}
                                            className="w-full h-full py-20 flex flex-col items-center justify-center cursor-pointer group/upload"
                                        >
                                            <div className="w-20 h-20 rounded-3xl bg-indigo-500/10 flex items-center justify-center mb-6 group-hover/upload:scale-110 group-hover/upload:bg-indigo-500/20 transition-all duration-500 shadow-2xl">
                                                <Upload size={32} className="text-indigo-400" />
                                            </div>
                                            <h3 className="text-xl font-bold text-white mb-2">Upload Analysis Material</h3>
                                            <p className="text-slate-500 text-center max-w-xs">Drag and drop any image or click to browse. Supported: JPG, PNG, WEBP.</p>
                                            <input 
                                                ref={fileInputRef}
                                                type="file" 
                                                accept="image/*"
                                                className="hidden"
                                                onChange={(e) => e.target.files && handleFileSelect(e.target.files[0])}
                                            />
                                        </div>
                                    ) : (
                                        <div className="relative w-full h-full flex items-center justify-center p-4">
                                            <img 
                                                src={results?.annotated_image || selectedImage} 
                                                alt="Preview" 
                                                className="max-h-[600px] w-auto rounded-2xl shadow-2xl object-contain border border-white/10"
                                            />
                                            {isAnalyzing && (
                                                <div className="absolute inset-0 bg-[#020617]/60 backdrop-blur-sm flex items-center justify-center z-10 rounded-2xl">
                                                    <div className="flex flex-col items-center gap-6">
                                                        <div className="relative">
                                                            <div className="w-16 h-16 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin"></div>
                                                            <div className="absolute inset-0 flex items-center justify-center">
                                                                <RefreshCw size={24} className="text-indigo-400 animate-pulse" />
                                                            </div>
                                                        </div>
                                                        <div className="text-center">
                                                            <h4 className="text-lg font-bold text-white mb-1">Analyzing with AI</h4>
                                                            <p className="text-sm text-slate-400">Processing frame using YOLOv8...</p>
                                                        </div>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </div>
                            
                            {/* Controls */}
                            <div className="flex items-center gap-4">
                                {!results ? (
                                    <button 
                                        onClick={analyzeImage}
                                        disabled={!selectedImage || isAnalyzing}
                                        className="btn-premium flex-1 flex items-center justify-center gap-2 group disabled:opacity-50 disabled:grayscale disabled:hover:scale-100"
                                    >
                                        <Camera size={20} className="group-hover:rotate-12 transition-transform" />
                                        <span>Start AI Detection</span>
                                    </button>
                                ) : (
                                    <button 
                                        onClick={() => { setSelectedImage(null); setResults(null); }}
                                        className="btn-premium bg-slate-800 from-slate-800 to-slate-900 border border-white/10 flex-1 flex items-center justify-center gap-2 group"
                                    >
                                        <RefreshCw size={20} className="group-hover:rotate-180 transition-transform duration-700" />
                                        <span>Process New Frame</span>
                                    </button>
                                )}
                                <button className="p-4 glass-card rounded-2xl text-slate-400 hover:text-white transition-colors border-white/5">
                                    <Download size={22} />
                                </button>
                            </div>
                        </div>

                        {/* Stats Panel */}
                        <div className="space-y-6">
                            {/* Overview stats */}
                            <div className="grid grid-cols-2 gap-4">
                                <div className="glass-card p-6 rounded-[2rem] border-white/5 relative overflow-hidden group">
                                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                                        <CheckCircle2 size={48} className="text-indigo-500" />
                                    </div>
                                    <p className="text-xs font-bold text-indigo-400 uppercase tracking-widest mb-1">Detection</p>
                                    <h5 className="text-xs text-slate-500 mb-3">Total Objects</h5>
                                    <p className="text-3xl font-black text-white">{results?.total_detections || 0}</p>
                                </div>
                                <div className="glass-card p-6 rounded-[2rem] border-white/5 relative overflow-hidden group">
                                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                                        <AlertTriangle size={48} className="text-violet-500" />
                                    </div>
                                    <p className="text-xs font-bold text-violet-400 uppercase tracking-widest mb-1">Violations</p>
                                    <h5 className="text-xs text-slate-500 mb-3">Alert Count</h5>
                                    <p className="text-3xl font-black text-white">{results?.violations?.total_violations || 0}</p>
                                </div>
                            </div>

                            {/* Detailed breakdown */}
                            <div className="glass-card p-8 rounded-[2.5rem] border-white/5 space-y-8">
                                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                                    <BarChart3 size={20} className="text-indigo-400" />
                                    Safety Analytics
                                </h3>

                                <div className="space-y-6">
                                    {/* Confidence Meter */}
                                    <div className="space-y-3">
                                        <div className="flex justify-between items-end">
                                            <div>
                                                <p className="text-sm font-semibold text-slate-300">Model Confidence</p>
                                                <p className="text-[10px] text-slate-500 uppercase tracking-wider">System Accuracy Index</p>
                                            </div>
                                            <span className="text-xl font-black text-indigo-400">{avgConfidence}%</span>
                                        </div>
                                        <div className="h-3 w-full bg-slate-900/50 rounded-full border border-white/5 overflow-hidden p-0.5">
                                            <div 
                                                className="h-full bg-gradient-to-r from-indigo-600 to-indigo-400 rounded-full transition-all duration-1000 ease-out shadow-[0_0_15px_rgba(99,102,241,0.3)]"
                                                style={{ width: `${avgConfidence}%` }}
                                            ></div>
                                        </div>
                                    </div>

                                    {/* Circular Progress (Simplified for UI layout) */}
                                    <div className="flex items-center gap-6 p-4 rounded-3xl bg-white/5 border border-white/5">
                                        <div className="relative w-20 h-20">
                                            <svg className="w-full h-full transform -rotate-90">
                                                <circle cx="40" cy="40" r="35" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="6" />
                                                <circle 
                                                    cx="40" 
                                                    cy="40" 
                                                    r="35" 
                                                    fill="none" 
                                                    stroke="#6366f1" 
                                                    strokeWidth="6"
                                                    strokeDasharray={220}
                                                    strokeDashoffset={220 - (220 * (withHelmet / Math.max(helmetDetections.length, 1)))}
                                                    className="transition-all duration-1000"
                                                    strokeLinecap="round"
                                                />
                                            </svg>
                                            <div className="absolute inset-0 flex items-center justify-center">
                                                <span className="text-sm font-bold">{Math.round((withHelmet / Math.max(helmetDetections.length, 1)) * 100)}%</span>
                                            </div>
                                        </div>
                                        <div>
                                            <p className="text-sm font-bold text-white">Safe Ratio</p>
                                            <p className="text-xs text-slate-500">Compliance score for current frame</p>
                                        </div>
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="p-4 rounded-2xl bg-emerald-500/5 border border-emerald-500/10">
                                        <p className="text-[10px] text-emerald-500 font-bold uppercase tracking-wider mb-1">With Helmet</p>
                                        <p className="text-2xl font-black text-white">{withHelmet}</p>
                                    </div>
                                    <div className="p-4 rounded-2xl bg-red-500/5 border border-red-500/10">
                                        <p className="text-[10px] text-red-500 font-bold uppercase tracking-wider mb-1">Violations</p>
                                        <p className="text-2xl font-black text-white">{withoutHelmet}</p>
                                    </div>
                                </div>
                            </div>

                            {/* Alert Log */}
                            <div className="glass-card p-6 rounded-[2.5rem] border-white/5">
                                <h3 className="text-sm font-bold text-slate-400 mb-4 px-2 uppercase tracking-widest">Recent Alerts</h3>
                                <div className="space-y-3">
                                    {results?.violations?.violations?.length > 0 ? (
                                        results.violations.violations.map((v: any, i: number) => (
                                            <div key={i} className="flex items-center gap-3 p-3 rounded-2xl bg-white/5 border border-white/5 animate-in slide-in-from-right duration-500" style={{ animationDelay: `${i * 100}ms` }}>
                                                <div className="w-8 h-8 rounded-xl bg-red-500/10 flex items-center justify-center text-red-400">
                                                    <AlertTriangle size={16} />
                                                </div>
                                                <div className="flex-1">
                                                    <p className="text-xs font-bold text-white">{v.type}</p>
                                                    <p className="text-[10px] text-slate-500">{v.location || 'Section A-4'}</p>
                                                </div>
                                                <span className="text-[10px] font-bold text-red-400">HIGH</span>
                                            </div>
                                        ))
                                    ) : (
                                        <div className="text-center py-4">
                                            <div className="w-12 h-12 rounded-full bg-slate-900 mx-auto flex items-center justify-center mb-2">
                                                <ShieldCheck size={20} className="text-slate-700" />
                                            </div>
                                            <p className="text-xs text-slate-600">No active violations detected</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Error Overlay */}
            {error && (
                <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-xl flex items-center justify-center z-[100] p-6">
                    <div className="max-w-md w-full glass-card p-10 rounded-[3rem] text-center border-red-500/20 shadow-[0_0_50px_rgba(239,68,68,0.1)]">
                        <div className="w-20 h-20 bg-red-500/10 rounded-3xl flex items-center justify-center mx-auto mb-6 text-red-500">
                            <AlertTriangle size={40} />
                        </div>
                        <h3 className="text-2xl font-black text-white mb-2 tracking-tight">System Exception</h3>
                        <p className="text-slate-400 mb-10 leading-relaxed">{error}</p>
                        <button 
                            onClick={() => setError(null)}
                            className="w-full py-4 bg-white text-slate-950 rounded-2xl font-bold hover:bg-slate-200 transition-colors"
                        >
                            Acknowledge
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
