import time
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from matplotlib.ticker import EngFormatter
from crypto.rsa import RSA
from crypto.ecc import ECC
from crypto.dilithium import Dilithium
from crypto.falcon import Falcon

class CryptoBenchmark:
    def __init__(self):
        self.warmup_iterations = 3
        self.measurement_iterations = 10
        self.test_data = b"Benchmark test data for cryptographic comparison"
        self.results = []
        self.results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'results'))
        os.makedirs(self.results_dir, exist_ok=True)
        self.min_throughput = 0.1
        
    def _warmup(self, crypto_class):
        crypto = crypto_class()
        for _ in range(self.warmup_iterations):
            try:
                sig = crypto.sign(self.test_data)
                crypto.verify(self.test_data, sig)
            except Exception as e:
                print(f"  Warmup warning: {str(e)}")
        return crypto

    def _measure_operation(self, operation, crypto, iterations):
        times = []
        results = []
        for _ in range(iterations):
            try:
                start = time.perf_counter_ns()
                result = operation(crypto)
                elapsed = (time.perf_counter_ns() - start) / 1_000_000  # ms
                times.append(elapsed)
                results.append(result)
            except Exception as e:
                print(f"  Measurement warning: {str(e)}")
                continue
        
        if not times:
            return float('nan'), None
        
        return statistics.median(times), results[-1] if results else None

    def _measure_throughput(self, crypto_class, duration=1.0, timeout=30.0):
        crypto = crypto_class()
        operations = 0
        start = time.perf_counter()
        end_time = start + duration
        timeout_time = start + timeout
        
        while time.perf_counter() < end_time and time.perf_counter() < timeout_time:
            try:
                sig = crypto.sign(self.test_data)
                if crypto.verify(self.test_data, sig):
                    operations += 1
            except Exception as e:
                print(f"  Throughput warning: {str(e)}")
                break
        
        if operations == 0 or time.perf_counter() >= timeout_time:
            try:
                sig_start = time.perf_counter()
                sig = crypto.sign(self.test_data)
                if crypto.verify(self.test_data, sig):
                    operations = 1
                    measured_time = time.perf_counter() - sig_start
                    return max(1/measured_time, self.min_throughput)
            except Exception as e:
                print(f"  Throughput fallback warning: {str(e)}")
                return self.min_throughput
        
        measured_throughput = operations / min(duration, time.perf_counter() - start)
        return max(measured_throughput, self.min_throughput)

    def benchmark_algorithm(self, name, crypto_class, security_level):
        print(f"\nBenchmarking {name}...")
        result = {
            'Algorithm': name,
            'Security (bits)': security_level,
            'KeyGen (ms)': float('nan'),
            'Sign (ms)': float('nan'),
            'Verify (ms)': float('nan'),
            'Throughput (tx/s)': float('nan'),
            'Latency (ms)': float('nan')
        }
        
        try:
            print("  Measuring key generation...", end=' ', flush=True)
            keygen_time, crypto = self._measure_operation(
                lambda _: crypto_class(), None, self.measurement_iterations
            )
            result['KeyGen (ms)'] = keygen_time
            print(f"{keygen_time:.2f} ms")
            
            if not crypto:
                crypto = crypto_class()
                
            print("  Measuring signing...", end=' ', flush=True)
            sign_time, sig = self._measure_operation(
                lambda c: c.sign(self.test_data), crypto, self.measurement_iterations
            )
            result['Sign (ms)'] = sign_time
            print(f"{sign_time:.2f} ms")
            
            print("  Measuring verification...", end=' ', flush=True)
            verify_time, _ = self._measure_operation(
                lambda c: c.verify(self.test_data, sig), crypto, self.measurement_iterations
            )
            result['Verify (ms)'] = verify_time
            print(f"{verify_time:.2f} ms")
            
            print("  Measuring throughput...", end=' ', flush=True)
            throughput = self._measure_throughput(crypto_class)
            result['Throughput (tx/s)'] = throughput
            print(f"{throughput:.2f} tx/s")
            
            result['Latency (ms)'] = sign_time + verify_time
            
        except Exception as e:
            print(f"\n  Error benchmarking {name}: {str(e)}")
        
        self.results.append(result)
        return result

    def run_all_benchmarks(self):
        print("Starting cryptographic benchmarks...")
        
        algorithms = [
            ("RSA-2048", RSA, 112),
            ("ECC-256", ECC, 128),
            ("Dilithium", Dilithium, 180),
            ("Falcon", Falcon, 192)
        ]
        
        for name, algo_class, security in algorithms:
            self.benchmark_algorithm(name, algo_class, security)
            
        return pd.DataFrame(self.results)

    def save_results(self, df):
        csv_path = os.path.join(self.results_dir, 'crypto_benchmark_results.csv')
        df.to_csv(csv_path, index=False)
        print(f"\nResults saved to: {csv_path}")

class CryptoVisualizer:
    def __init__(self, benchmark_data):
        self.df = benchmark_data.dropna()
        self.results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'results'))
        os.makedirs(self.results_dir, exist_ok=True)
        self._setup_plot_style()
        
    def _setup_plot_style(self):
        plt.style.use('seaborn')
        sns.set_style("whitegrid", {
            'axes.edgecolor': '0.2',
            'axes.labelcolor': '0.2',
            'text.color': '0.2',
            'xtick.color': '0.2',
            'ytick.color': '0.2',
            'grid.color': '0.9'
        })
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['savefig.dpi'] = 300
        self.palette = sns.color_palette("husl", n_colors=len(self.df))

    def _save_figure(self, fig, filename):
        path = os.path.join(self.results_dir, filename)
        fig.tight_layout()
        fig.savefig(path, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        print(f"  Saved: {filename}")

    def plot_keygen_time(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x='Algorithm', y='KeyGen (ms)', data=self.df, palette=self.palette, ax=ax)
        ax.set_yscale('log')
        ax.set_title('Key Generation Time (log scale)')
        ax.set_ylabel('Time (ms)')
        ax.yaxis.set_major_formatter(EngFormatter())
        self._save_figure(fig, 'crypto_keygen_time.png')

    def plot_throughput(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x='Algorithm', y='Throughput (tx/s)', data=self.df, palette=self.palette, ax=ax)
        ax.set_title('Transaction Throughput')
        ax.set_ylabel('Operations per second')
        ax.yaxis.set_major_formatter(EngFormatter())
        self._save_figure(fig, 'crypto_throughput.png')

    def plot_sign_verify(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        melted = self.df.melt(id_vars=['Algorithm'], 
                            value_vars=['Sign (ms)', 'Verify (ms)'],
                            var_name='Operation', value_name='Time (ms)')
        sns.barplot(x='Algorithm', y='Time (ms)', hue='Operation',
                   data=melted, ax=ax, palette='coolwarm')
        ax.set_title('Signing vs Verification Times')
        ax.set_ylabel('Time (ms)')
        self._save_figure(fig, 'crypto_sign_verify.png')

    def plot_security_tradeoff(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = sns.scatterplot(
            x='Security (bits)', y='Latency (ms)', 
            size='Throughput (tx/s)', hue='Algorithm',
            data=self.df, sizes=(100, 400), palette=self.palette,
            ax=ax, legend='brief'
        )
        ax.set_title('Security vs Performance Trade-off')
        ax.set_xlabel('Security Level (bits)')
        ax.set_ylabel('Latency (ms)')
        
        for idx, row in self.df.iterrows():
            ax.text(
                row['Security (bits)'], row['Latency (ms)'], row['Algorithm'],
                fontsize=9, ha='center', va='bottom'
            )
        
        self._save_figure(fig, 'crypto_security_tradeoff.png')

    def plot_radar_chart(self):
        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'polar': True})
        categories = ['KeyGen', 'Sign', 'Verify', 'Throughput', 'Security']
        
        norm_data = self.df.copy()
        norm_data['KeyGen'] = 1 / self.df['KeyGen (ms)']
        norm_data['Sign'] = 1 / self.df['Sign (ms)']
        norm_data['Verify'] = 1 / self.df['Verify (ms)']
        norm_data['Throughput'] = self.df['Throughput (tx/s)'] / self.df['Throughput (tx/s)'].max()
        norm_data['Security'] = self.df['Security (bits)'] / self.df['Security (bits)'].max()
        
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]
        
        for idx, row in norm_data.iterrows():
            values = row[categories].tolist()
            values += values[:1]
            ax.plot(angles, values, label=row['Algorithm'], 
                   color=self.palette[idx], linewidth=2)
            ax.fill(angles, values, color=self.palette[idx], alpha=0.1)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_title('Normalized Performance Comparison')
        ax.legend(bbox_to_anchor=(1.2, 1), loc='upper left')
        self._save_figure(fig, 'crypto_radar_chart.png')

    def generate_all_plots(self):
        print("\nGenerating visualizations...")
        self.plot_keygen_time()
        self.plot_throughput()
        self.plot_sign_verify()
        self.plot_security_tradeoff()
        self.plot_radar_chart()
        print("Visualizations completed!")

def main():
    try:
        benchmark = CryptoBenchmark()
        results = benchmark.run_all_benchmarks()
        benchmark.save_results(results)
        
        print("\nBenchmark Results:")
        print(results.to_string(index=False))
        
        if not results.empty:
            visualizer = CryptoVisualizer(results)
            visualizer.generate_all_plots()
            print("\nBenchmark completed successfully!")
            print(f"Results saved to: {benchmark.results_dir}")
        else:
            print("\nBenchmark failed - no results generated")
            
    except Exception as e:
        print(f"\nError during benchmark: {str(e)}")

if __name__ == "__main__":
    main()