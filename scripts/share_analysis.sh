#!/bin/bash
# ========================================
# 一键生成分析分享文件
# ========================================

# 使用方法:
# ./scripts/share_analysis.sh notebooks/your_analysis.ipynb

NOTEBOOK="$1"

if [ -z "$NOTEBOOK" ]; then
    echo "❌ 错误: 请提供 notebook 文件"
    echo "用法: $0 <notebook.ipynb>"
    echo "示例: $0 notebooks/analysis.ipynb"
    exit 1
fi

if [ ! -f "$NOTEBOOK" ]; then
    echo "❌ 错误: 文件不存在: $NOTEBOOK"
    exit 1
fi

BASENAME=$(basename "$NOTEBOOK" .ipynb)
DIR=$(dirname "$NOTEBOOK")
OUTPUT_DIR="${DIR}/shared_${BASENAME}"

echo "📤 准备分享: $NOTEBOOK"
echo "📁 输出目录: $OUTPUT_DIR"
echo ""

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 1. HTML（无代码，适合快速分享）
echo "📄 生成 HTML（无代码）..."
jupyter nbconvert --to html \
    --no-input \
    --no-prompt \
    --TagRemovePreprocessor.enabled=True \
    "$NOTEBOOK" \
    --output-dir="$OUTPUT_DIR" \
    --output="${BASENAME}.html"

if [ $? -eq 0 ]; then
    echo "   ✅ ${BASENAME}.html"
else
    echo "   ❌ HTML 生成失败（可能需要先 Clear Outputs）"
fi

# 2. HTML（含代码，适合技术人员）
echo "📄 生成 HTML（含代码）..."
jupyter nbconvert --to html "$NOTEBOOK" \
    --output-dir="$OUTPUT_DIR" \
    --output="${BASENAME}_with_code.html"

if [ $? -eq 0 ]; then
    echo "   ✅ ${BASENAME}_with_code.html"
else
    echo "   ❌ HTML（含代码）生成失败"
fi

# 3. Markdown
echo "📄 生成 Markdown..."
jupyter nbconvert --to markdown "$NOTEBOOK" \
    --output-dir="$OUTPUT_DIR" \
    --output="${BASENAME}.md"

if [ $? -eq 0 ]; then
    echo "   ✅ ${BASENAME}.md"
else
    echo "   ❌ Markdown 生成失败"
fi

# 4. Python 脚本
echo "📄 生成 Python 脚本..."
jupyter nbconvert --to script "$NOTEBOOK" \
    --output-dir="$OUTPUT_DIR" \
    --output="${BASENAME}.py"

if [ $? -eq 0 ]; then
    echo "   ✅ ${BASENAME}.py"
else
    echo "   ❌ Python 脚本生成失败"
fi

# 5. 创建 README
echo "📄 生成 README..."
cat > "$OUTPUT_DIR/README.md" << EOF
# 📊 ${BASENAME} - 分析分享包

**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')
**原始文件**: $NOTEBOOK

---

## 📦 包含文件

1. **${BASENAME}.html** - HTML 版本（无代码）
   - 适合：快速查看、邮件分享
   - 包含：所有图表、表格、输出
   - 打开方式：直接用浏览器打开

2. **${BASENAME}_with_code.html** - HTML 版本（含代码）
   - 适合：技术人员学习参考
   - 包含：完整代码和输出
   - 打开方式：直接用浏览器打开

3. **${BASENAME}.md** - Markdown 版本
   - 适合：嵌入文档系统、GitHub
   - 包含：代码和输出文本
   - 打开方式：任何文本编辑器、Markdown 阅读器

4. **${BASENAME}.py** - Python 脚本
   - 适合：直接运行、代码复用
   - 包含：纯代码（无输出）
   - 运行方式：python ${BASENAME}.py

---

## 🚀 使用建议

### 快速分享给领导/同事
→ 使用 **${BASENAME}.html**（邮件附件或内网链接）

### 技术交流/学习
→ 使用 **${BASENAME}_with_code.html** 或 **${BASENAME}.py**

### 文档归档
→ 使用 **${BASENAME}.md**（便于搜索、版本控制）

---

## 💡 注意事项

- ✅ HTML 文件可以离线打开
- ✅ Plotly 图表在 HTML 中仍然可交互
- ⚠️ 如果包含大量图片/数据，文件可能较大
- ⚠️ 敏感数据请谨慎分享

---

**祝分享顺利！** 🎉
EOF

echo "   ✅ README.md"

# 6. 打包（可选）
echo ""
echo "📦 是否创建压缩包？(y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    ARCHIVE="${DIR}/${BASENAME}_share_$(date '+%Y%m%d_%H%M%S').tar.gz"
    
    echo "📦 创建压缩包..."
    tar -czf "$ARCHIVE" -C "$(dirname $OUTPUT_DIR)" "$(basename $OUTPUT_DIR)"
    
    if [ $? -eq 0 ]; then
        echo "   ✅ $ARCHIVE"
        echo ""
        echo "📊 文件大小:"
        du -h "$ARCHIVE"
    else
        echo "   ❌ 压缩包创建失败"
    fi
fi

echo ""
echo "=" 
echo "✅ 完成！"
echo "="
echo ""
echo "📁 分享文件位置: $OUTPUT_DIR"
echo ""
echo "📤 下一步:"
echo "  1. 查看生成的文件"
echo "  2. 选择合适的格式分享"
echo "  3. 如需压缩包，运行时选择 'y'"
echo ""
echo "💡 提示: 用浏览器打开 ${BASENAME}.html 预览效果"
echo ""
