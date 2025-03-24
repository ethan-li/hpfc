#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HPFC工具 - 中文使用示例

这个脚本展示了如何使用hpfc工具来比较目录，
并生成报告，同时展示了命令行参数的设置。
"""

import os
import sys
import tempfile
import shutil
import argparse
from pathlib import Path

# 将父目录添加到路径中，以便导入包
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.hpfc.core import DirectoryComparer


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='目录比较工具使用示例')
    parser.add_argument('--dir1', help='第一个目录路径（如果不指定将创建临时目录）')
    parser.add_argument('--dir2', help='第二个目录路径（如果不指定将创建临时目录）')
    parser.add_argument('--files', type=int, default=50, help='要创建的测试文件数量（默认50）')
    parser.add_argument('--no-progress', action='store_true', help='禁用进度条显示')
    parser.add_argument('--html', action='store_true', help='生成HTML报告')
    parser.add_argument('--report', help='报告输出路径')
    parser.add_argument('--chunk-size', type=int, default=8 * 1024 * 1024, help='文件分块大小（默认8MB）')
    parser.add_argument('--workers', type=int, help='并行处理的工作进程数')
    return parser.parse_args()


def create_test_directories(num_files=50):
    """创建两个测试目录，包含相同、不同和独有的文件"""
    print(f"正在创建测试目录，每个目录包含约 {num_files} 个文件...")
    
    # 创建临时目录
    dir1 = tempfile.mkdtemp(prefix="compare_demo_dir1_")
    dir2 = tempfile.mkdtemp(prefix="compare_demo_dir2_")
    
    print(f"目录1: {dir1}")
    print(f"目录2: {dir2}")
    
    # 在目录中创建子目录结构
    os.makedirs(os.path.join(dir1, "共同子目录", "深层目录"), exist_ok=True)
    os.makedirs(os.path.join(dir2, "共同子目录", "深层目录"), exist_ok=True)
    os.makedirs(os.path.join(dir1, "dir1独有目录"), exist_ok=True)
    os.makedirs(os.path.join(dir2, "dir2独有目录"), exist_ok=True)
    
    # 创建相同的文件（包括在子目录中）
    print("正在创建相同的文件...")
    for i in range(num_files // 2):
        # 根目录中的相同文件
        if i % 5 == 0:
            file_path1 = os.path.join(dir1, "共同子目录", f"相同文件_{i}.txt")
            file_path2 = os.path.join(dir2, "共同子目录", f"相同文件_{i}.txt")
        elif i % 7 == 0:
            file_path1 = os.path.join(dir1, "共同子目录", "深层目录", f"相同文件_{i}.txt")
            file_path2 = os.path.join(dir2, "共同子目录", "深层目录", f"相同文件_{i}.txt")
        else:
            file_path1 = os.path.join(dir1, f"相同文件_{i}.txt")
            file_path2 = os.path.join(dir2, f"相同文件_{i}.txt")
            
        with open(file_path1, "w", encoding="utf-8") as f:
            content = f"这是相同内容的文件 {i}\n" * 10
            f.write(content)
        with open(file_path2, "w", encoding="utf-8") as f:
            content = f"这是相同内容的文件 {i}\n" * 10
            f.write(content)
    
    # 创建内容不同的文件
    print("正在创建内容不同的文件...")
    for i in range(num_files // 4):
        if i % 3 == 0:
            file_path1 = os.path.join(dir1, "共同子目录", f"不同内容_{i}.txt")
            file_path2 = os.path.join(dir2, "共同子目录", f"不同内容_{i}.txt")
        else:
            file_path1 = os.path.join(dir1, f"不同内容_{i}.txt")
            file_path2 = os.path.join(dir2, f"不同内容_{i}.txt")
            
        with open(file_path1, "w", encoding="utf-8") as f:
            content = f"这是dir1中的内容，与dir2不同 {i}\n" * 5
            f.write(content)
        with open(file_path2, "w", encoding="utf-8") as f:
            content = f"这是dir2中的内容，与dir1不同 {i}\n" * 5
            f.write(content)
    
    # 创建dir1独有的文件
    print("正在创建dir1独有的文件...")
    for i in range(num_files // 8):
        if i % 2 == 0:
            file_path = os.path.join(dir1, "dir1独有目录", f"只在dir1存在_{i}.txt")
        else:
            file_path = os.path.join(dir1, f"只在dir1存在_{i}.txt")
            
        with open(file_path, "w", encoding="utf-8") as f:
            content = f"这个文件只存在于dir1 {i}\n" * 3
            f.write(content)
    
    # 创建dir2独有的文件
    print("正在创建dir2独有的文件...")
    for i in range(num_files // 8):
        if i % 2 == 0:
            file_path = os.path.join(dir2, "dir2独有目录", f"只在dir2存在_{i}.txt")
        else:
            file_path = os.path.join(dir2, f"只在dir2存在_{i}.txt")
            
        with open(file_path, "w", encoding="utf-8") as f:
            content = f"这个文件只存在于dir2 {i}\n" * 3
            f.write(content)
    
    # 创建一个大文件（用于测试分块处理）
    print("正在创建测试用大文件...")
    with open(os.path.join(dir1, "大文件.txt"), "w", encoding="utf-8") as f:
        content = "这是一个用于测试分块哈希比较的大文件\n" * 10000
        f.write(content)
    with open(os.path.join(dir2, "大文件.txt"), "w", encoding="utf-8") as f:
        content = "这是一个用于测试分块哈希比较的大文件\n" * 10000
        f.write(content)
    
    # 创建另一个大文件，但内容不同
    with open(os.path.join(dir1, "不同的大文件.txt"), "w", encoding="utf-8") as f:
        content = "这是dir1中的大文件，内容与dir2中的不同\n" * 10000
        f.write(content)
    with open(os.path.join(dir2, "不同的大文件.txt"), "w", encoding="utf-8") as f:
        content = "这是dir2中的大文件，内容与dir1中的不同\n" * 10000
        f.write(content)
    
    return dir1, dir2


def main():
    """主函数"""
    args = parse_args()
    created_dirs = False
    
    try:
        # 如果没有提供目录，则创建测试目录
        if not args.dir1 or not args.dir2:
            dir1, dir2 = create_test_directories(args.files)
            created_dirs = True
        else:
            dir1, dir2 = args.dir1, args.dir2
            if not os.path.isdir(dir1):
                print(f"错误：目录不存在 - {dir1}")
                return 1
            if not os.path.isdir(dir2):
                print(f"错误：目录不存在 - {dir2}")
                return 1
        
        print("\n" + "=" * 60)
        print("开始比较目录")
        print("=" * 60)
        print(f"目录 1: {dir1}")
        print(f"目录 2: {dir2}")
        print(f"使用进度条: {'否' if args.no_progress else '是'}")
        print(f"分块大小: {args.chunk_size / 1024 / 1024:.1f} MB")
        print(f"工作进程数: {args.workers if args.workers else '自动 (CPU 核心数)'}")
        print("=" * 60)
        
        # 创建比较器实例
        comparer = DirectoryComparer(
            dir1, 
            dir2, 
            chunk_size=args.chunk_size,
            max_workers=args.workers,
            show_progress=not args.no_progress
        )
        
        # 执行比较
        results = comparer.compare()
        
        # 整理并显示结果
        different_count = len(results["different_files"])
        missing_count = len(results["missing_files"])
        extra_count = len(results["extra_files"])
        identical_count = len(results["identical_files"])
        error_count = len(results["error_files"])
        
        print("\n" + "=" * 60)
        print("比较结果摘要")
        print("=" * 60)
        print(f"相同文件: {identical_count}")
        print(f"不同文件: {different_count}")
        print(f"缺失文件 (在dir1中存在但在dir2中不存在): {missing_count}")
        print(f"额外文件 (在dir2中存在但在dir1中不存在): {extra_count}")
        print(f"错误文件: {error_count}")
        print(f"处理时间: {results['time_elapsed']:.2f} 秒")
        print("=" * 60)
        
        # 生成报告
        if args.html:
            report = comparer.generate_html_report(results)
            report_type = "HTML"
        else:
            report = comparer.generate_text_report(results)
            report_type = "文本"
        
        # 输出报告
        if args.report:
            with open(args.report, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n{report_type}报告已保存到: {args.report}")
        else:
            if not args.html:  # 仅在非HTML报告时打印到控制台
                print("\n详细报告:")
                print(report)
            else:
                report_path = os.path.join(os.getcwd(), "比较报告.html")
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"\nHTML报告已保存到: {report_path}")
    
    finally:
        # 如果使用的是自动创建的临时目录，则清理
        if created_dirs:
            print("\n正在清理临时目录...")
            shutil.rmtree(dir1, ignore_errors=True)
            shutil.rmtree(dir2, ignore_errors=True)
            print("清理完成！")


if __name__ == "__main__":
    sys.exit(main()) 