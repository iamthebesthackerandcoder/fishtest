"""
Worker Controller for Fishtest Worker GUI
Handles starting, stopping, and monitoring the fishtest worker process.
"""

import subprocess
import threading
import sys
import os
from pathlib import Path
import queue
import time

class WorkerController:
    def __init__(self):
        self.worker_process = None
        self.is_worker_running = False
        self.output_callback = None
        self.worker_dir = Path(__file__).resolve().parent / "worker"
        
    def is_running(self):
        """Check if worker is currently running"""
        return self.is_worker_running and self.worker_process and self.worker_process.poll() is None
        
    def start_worker(self, username, password, cores, output_callback=None):
        """Start the fishtest worker process"""
        if self.is_running():
            raise Exception("Worker is already running")
            
        self.output_callback = output_callback
        
        # Build command
        worker_script = self.worker_dir / "worker.py"
        if not worker_script.exists():
            raise Exception(f"Worker script not found: {worker_script}")
            
        cmd = [
            sys.executable, 
            str(worker_script),
            username, 
            password,
            "--concurrency", str(cores),
            "--protocol", "https",
            "--host", "tests.stockfishchess.org",
            "--port", "443"
        ]
        
        try:
            # Start the worker process
            self.worker_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                cwd=str(self.worker_dir)
            )
            
            self.is_worker_running = True
            
            # Start output monitoring thread
            self.output_thread = threading.Thread(target=self._monitor_output, daemon=True)
            self.output_thread.start()
            
            if self.output_callback:
                self.output_callback("Worker started successfully")
                
        except Exception as e:
            self.is_worker_running = False
            raise Exception(f"Failed to start worker: {e}")
            
    def stop_worker(self):
        """Stop the fishtest worker process"""
        if not self.is_running():
            return
            
        try:
            self.is_worker_running = False
            
            if self.worker_process:
                # Try graceful termination first
                self.worker_process.terminate()
                
                # Wait a bit for graceful shutdown
                try:
                    self.worker_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if it doesn't stop gracefully
                    self.worker_process.kill()
                    self.worker_process.wait()
                    
                self.worker_process = None
                
            if self.output_callback:
                self.output_callback("Worker stopped")
                
        except Exception as e:
            if self.output_callback:
                self.output_callback(f"Error stopping worker: {e}")
                
    def _monitor_output(self):
        """Monitor worker output in background thread"""
        try:
            while self.is_worker_running and self.worker_process:
                if self.worker_process.poll() is not None:
                    # Process has ended
                    break
                    
                try:
                    line = self.worker_process.stdout.readline()
                    if line and self.output_callback:
                        line = line.strip()
                        if line:  # Only send non-empty lines
                            self.output_callback(line)
                except Exception:
                    break
                    
        except Exception as e:
            if self.output_callback:
                self.output_callback(f"Output monitoring error: {e}")
        finally:
            # Worker process ended
            if self.is_worker_running:
                self.is_worker_running = False
                if self.output_callback:
                    return_code = self.worker_process.poll() if self.worker_process else None
                    if return_code is not None and return_code != 0:
                        self.output_callback(f"Worker process ended with error code: {return_code}")
                    else:
                        self.output_callback("Worker process ended")
