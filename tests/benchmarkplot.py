# benchmark.py
import time
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from matplotlib.ticker import EngFormatter

# --- Mock Cryptographic Implementations ---
class RSA:
    def sign(self, data): time.sleep(0.005); return b"sig";
    def verify(self, data, sig): time.sleep(0.0007); return True;
    def __init__(self): time.sleep(0.8);

class ECC:
    def sign(self, data): time.sleep(0.0004); return b"sig";
    def verify(self, data, sig): time.sleep(0.0017); return True;
    def __init__(self): time.sleep(0.0003);

class Dilithium:
    def sign(self, data): time.sleep(0.00006); return b"sig";
    def verify(self, data, sig): time.sleep(0.00002); return True;
    def __init__(self): time.sleep(0.00005);

class Falcon:
    def sign(self, data): time.sleep(0.00004); return b"sig";
    def verify(self, data, sig): time.sleep(0.00001); return True;
    def __init__(self): time.sleep(0.00003);
    
class SPHINCS:
    def sign(self, data): time.sleep(0.005); return b"sig";
    def verify(self, data, sig): time.sleep(0.001); return True;
    def __init__(self): time.sleep(0.0005);

# --- New Hybrid Class ---
class HybridFalconSPHINCS:
    def sign(self, data): time.sleep(0.00504); return b"sig";
    def verify(self, data, sig): time.sleep(0.00101); return True;
    def __init__(self): time.sleep(0.00053);

# --- Benchmark Classes (no changes) ---
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

    def _measure_throughput(self, crypto_class, num_operations=1000):
        crypto = crypto_class()
        operations = 0
        start_time = time.perf_counter()
        
        try:
            for _ in range(num_operations):
                sig = crypto.sign(self.test_data)
                if crypto.verify(self.test_data, sig):
                    operations += 1
        except Exception as e:
            print(f"  Throughput warning: {str(e)}")
            return self.min_throughput
        
        elapsed_time = time.perf_counter() - start_time
        
        if elapsed_time > 0:
            measured_throughput = operations / elapsed_time
            return max(measured_throughput, self.min_throughput)
        
        return self.min_throughput

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
            ("Falcon", Falcon, 192),
            ("SPHINCS+", SPHINCS, 192),
            ("Hybrid (Falcon+SPHINCS+)", HybridFalconSPHINCS, 192) # Added hybrid model
        ]
        
        for name, algo_class, security in algorithms:
            self.benchmark_algorithm(name, algo_class, security)
            
        return pd.DataFrame(self.results)

    def save_results(self, df):
        csv_path = os.path.join(self.results_dir, 'crypto_benchmark_results.csv')
        df.to_csv(csv_path, index=False)
        print(f"\nResults saved to: {csv_path}")

# --- Visualization Class (no changes) ---
class CryptoVisualizer:
    def __init__(self, benchmark_data):
        self.df = benchmark_data.dropna()
        self.results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'results'))
        os.makedirs(self.results_dir, exist_ok=True)
        print(f"\nVisualizations will be saved to: {self.results_dir}")
        self._setup_plot_style()
        
    def _setup_plot_style(self):
        """Configure consistent plot styling"""
        sns.set_theme(style="whitegrid")
        plt.rcParams.update({
            'font.family': 'serif',
            'figure.dpi': 300,
            'savefig.dpi': 300,
            'axes.edgecolor': '0.2',
            'axes.labelcolor': '0.2',
            'text.color': '0.2',
            'xtick.color': '0.2',
            'ytick.color': '0.2',
            'grid.color': '0.9'
        })
        self.palette = sns.color_palette("husl", n_colors=len(self.df))

    def _save_figure(self, fig, filename, title_suffix=""):
        """Save figure with error handling"""
        try:
            path = os.path.join(self.results_dir, filename)
            fig.tight_layout()
            fig.savefig(path, bbox_inches='tight', pad_inches=0.1, dpi=300)
            plt.close(fig)
            print(f"  Successfully saved: {filename}")
            return True
        except Exception as e:
            print(f"  Error saving {filename}: {str(e)}")
            plt.close(fig)
            return False

    def create_results_table_image(self):
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.axis('off')
        
        display_df = self.df.copy()
        for col in ['KeyGen (ms)', 'Sign (ms)', 'Verify (ms)', 'Throughput (tx/s)', 'Latency (ms)']:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}")
        
        table = ax.table(
            cellText=display_df.values,
            colLabels=display_df.columns,
            cellLoc='center',
            loc='center',
            colColours=['#f7f7f7']*len(display_df.columns))
        
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.5)
        
        ax.set_title('Cryptographic Algorithm Benchmark Results', fontsize=14, pad=20)
        
        return self._save_figure(fig, 'crypto_results_table.png')

    def plot_keygen_time(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Algorithm', y='KeyGen (ms)', data=self.df, 
                    hue='Algorithm', palette=self.palette, ax=ax)
        
        ax.set_yscale('log')
        ax.set_title('Key Generation Time (log scale)', pad=20, fontsize=14)
        ax.set_ylabel('Time (ms)', fontsize=12)
        ax.set_xlabel('')
        ax.yaxis.set_major_formatter(EngFormatter())
        return self._save_figure(fig, 'crypto_keygen_time.png')

    def plot_sign_verify_times(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        melted = self.df.melt(id_vars=['Algorithm'], 
                            value_vars=['Sign (ms)', 'Verify (ms)'],
                            var_name='Operation', value_name='Time (ms)')
        sns.barplot(x='Algorithm', y='Time (ms)', hue='Operation',
                    data=melted, ax=ax, palette='coolwarm')
        
        ax.set_yscale('log')
        ax.set_title('Signing vs Verification Times (log scale)', pad=20, fontsize=14)
        ax.set_ylabel('Time (ms)', fontsize=12)
        ax.set_xlabel('')
        return self._save_figure(fig, 'crypto_sign_verify_times.png')

    def plot_throughput(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Algorithm', y='Throughput (tx/s)', data=self.df,
                    hue='Algorithm', palette=self.palette, ax=ax)
        
        ax.set_title('Transaction Throughput', pad=20, fontsize=14)
        ax.set_ylabel('Operations per second', fontsize=12)
        ax.set_xlabel('')
        ax.yaxis.set_major_formatter(EngFormatter())
        return self._save_figure(fig, 'crypto_throughput.png')

    def plot_latency(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Algorithm', y='Latency (ms)', data=self.df,
                    hue='Algorithm', palette=self.palette, ax=ax)
        
        ax.set_yscale('log')
        ax.set_title('End-to-End Latency (log scale)', pad=20, fontsize=14)
        ax.set_ylabel('Time (ms)', fontsize=12)
        ax.set_xlabel('')
        ax.yaxis.set_major_formatter(EngFormatter())
        return self._save_figure(fig, 'crypto_latency.png')

    def generate_all_plots(self):
        print("\nGenerating visualizations...")
        success = True
        success &= self.create_results_table_image()
        success &= self.plot_keygen_time()
        success &= self.plot_sign_verify_times()
        success &= self.plot_throughput()
        success &= self.plot_latency()
        
        if success:
            print("\nAll visualizations generated successfully!")
            print(f"Check the results directory: {self.results_dir}")
        else:
            print("\nSome visualizations failed to generate")
        return success

def main():
    try:
        benchmark = CryptoBenchmark()
        results = benchmark.run_all_benchmarks()
        
        benchmark.save_results(results)
        
        print("\nBenchmark Results:")
        print(results.to_string(index=False))
        
        if not results.empty:
            visualizer = CryptoVisualizer(results)
            if not visualizer.generate_all_plots():
                print("\nWarning: Some visualizations failed to generate")
            print("\nBenchmark completed!")
            print(f"Results directory: {os.path.abspath(benchmark.results_dir)}")
        else:
            print("\nBenchmark failed - no results generated")
            
    except Exception as e:
        print(f"\nError during benchmark: {str(e)}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()