
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdarg.h>

#include <qrencode.h>

void *die(const char *fmt, ...)
{
	va_list ap;
	va_start(ap, fmt);
	vfprintf(stderr, fmt, ap);
	fprintf(stderr, "\n");
	va_end(ap);
	exit(EXIT_FAILURE);
}

typedef struct
{
	void (*node)(int, int, int);
	void (*startpoly)(int, int, int);
	void (*endpoly)(int, int, int);
	void (*start)(int);
	void (*end)(int);

} vector_plugin_t;

enum
{
	TOP = 1,
	RIGHT = 2,
	BOTTOM = 4,
	LEFT = 8,
};

void pgf_node(int x, int y, int qrsize)
{
	printf("\\pgflineto{\\pgfxy(%d,%d)}", x, qrsize-y);
}

void pgf_startpoly(int x, int y, int qrsize)
{
	printf("\\pgfmoveto{\\pgfxy(%d,%d)}", x, qrsize-y);
}

void pgf_endpoly(int x, int y, int qrsize)
{
	printf("\\pgfclosepath\n");
}

void pgf_start(int qrsize)
{
	printf("\\begin{pgfmagnify}{%.5f}{%5f}", 1./qrsize, 1./qrsize);
}

void pgf_end(int qrsize)
{
	printf("\\pgffill\n");
	printf("\\end{pgfmagnify}\n");
}

void svg_node(int x, int y, int qrsize)
{
	printf("L %d %d ", x, qrsize-y);
}

void svg_startpoly(int x, int y, int qrsize)
{
	printf("M %d %d ", x, qrsize-y);
}

void svg_endpoly(int x, int y, int qrsize)
{
	printf("z ");
}

void svg_start(int qrsize)
{
	printf("");
}

void svg_end(int qrsize)
{
	printf("");
}

vector_plugin_t pgf = { pgf_node, pgf_startpoly, pgf_endpoly, pgf_start, pgf_end };
vector_plugin_t svg = { svg_node, pgf_startpoly, pgf_endpoly, svg_start, svg_end };

/*
static void print_code(QRcode *qr)
{
	for (int y=0; y < qr->width; y++)
	{
		for (int x=0; x < qr->width; x++)
			printf( "%c%s%c", qr->data[y*qr->width+x]&(TOP|LEFT)?'*':' ', qr->data[y*qr->width+x]&TOP ? "---" : "   ", qr->data[y*qr->width+x]&(TOP|RIGHT)?'*':' ');
		printf("\n");
		for (int x=0; x < qr->width; x++)
			printf( "%c   %c", qr->data[y*qr->width+x]&LEFT?'|':' ', qr->data[y*qr->width+x]&RIGHT?'|':' ' );
		printf("\n");
		for (int x=0; x < qr->width; x++)
			printf( "%c   %c", qr->data[y*qr->width+x]&LEFT?'|':' ', qr->data[y*qr->width+x]&RIGHT?'|':' ' );
		printf("\n");
		for (int x=0; x < qr->width; x++)
			printf( "%c%s%c", qr->data[y*qr->width+x]&(BOTTOM|LEFT)?'*':' ', qr->data[y*qr->width+x]&BOTTOM ? "---" : "   ", qr->data[y*qr->width+x]&(BOTTOM|RIGHT)?'*':' ');
		printf("\n");
	}
}
*/

static int has_edge(QRcode *qr, int x, int y, int dir)
{
	if (dir & (RIGHT|BOTTOM)) x--;
	if (dir & (BOTTOM|LEFT))  y--;

	if ( (x < 0) || (x >= qr->width) || (y < 0) || (y >= qr->width) )
		return 0;
	else
		return qr->data[y*qr->width+x] & dir;
}

static void clear_edge(QRcode *qr, int x, int y, int dir)
{
	if (dir & (RIGHT|BOTTOM)) x--;
	if (dir & (BOTTOM|LEFT))  y--;

	if ( (x < 0) || (x >= qr->width) || (y < 0) || (y >= qr->width) )
		return;

	qr->data[y*qr->width+x] &= ~dir;
}

static int next(int dir)
{
	if (dir == LEFT)
		return TOP;
	else
		return dir*2;
}

static int previous(int dir)
{
	if (dir == TOP)
		return LEFT;
	else
		return dir/2;
}

/* prints region and erases it from the qr code */
static void print_region(QRcode *qr, int x, int y, int dir, vector_plugin_t *plug)
{
	int start_x = x, start_y = y;
	struct { int x, y; } move[9] = { [TOP]={1,0}, [RIGHT]={0,1}, [BOTTOM]={-1,0}, [LEFT]={0,-1} };

	plug->startpoly(x, y, qr->width);

	do
	{
		if (!has_edge(qr, x, y, dir))
		{
			plug->node(x, y, qr->width);

			if (has_edge(qr, x, y, next(dir)))
				dir = next(dir);
			else
				dir = previous(dir);
		}

		clear_edge(qr, x, y, dir);
		x += move[dir].x;
		y += move[dir].y;

	}
	while ( (x != start_x) || (y != start_y) );

	plug->endpoly(start_x, start_y, qr->width);
}

static void print_regions(QRcode *qr, vector_plugin_t *plug)
{
	plug->start(qr->width);

	for (int y=0; y <= qr->width; y++)
		for (int x=0; x <= qr->width; x++)
		{
			if (has_edge(qr, x, y, TOP))
				print_region(qr, x, y, TOP, plug);

			if (has_edge(qr, x, y, RIGHT))
				print_region(qr, x, y, RIGHT, plug);
		}

	plug->end(qr->width);
}

static void encode_borders(QRcode *qr)
{
	for (int i=0; i < qr->width*qr->width; i++)
		qr->data[i] = (qr->data[i]&1)*0x80;

	for (int i=0; i < qr->width*qr->width; i++)
	{
		if (! (qr->data[i] & 0x80) )
			continue;

		if ( (i < qr->width)                || !qr->data[i-qr->width] )
			qr->data[i] |= TOP;

		if ( (i >= qr->width*(qr->width-1)) || !qr->data[i+qr->width] )
			qr->data[i] |= BOTTOM;

		if ( !(i % qr->width)               || !qr->data[i-1]         )
			qr->data[i] |= LEFT;

		if ( !((i+1) % qr->width)           || !qr->data[i+1]         )
			qr->data[i] |= RIGHT;
	}

	for (int i=0; i < qr->width*qr->width; i++)
		qr->data[i] &= ~0x80;
}

#define QR_CODE_MAX_SIZE (7090)
int main(int argc, char **argv)
{
	vector_plugin_t *plug;

	if      ( (argc >= 2) && (strcmp(argv[1], "-svg")==0) )
		plug = &svg;
	else if ( (argc >= 2) && (strcmp(argv[1], "-pgf")==0) )
		plug = &pgf;
	else
		die("Usage: %s -svg|-pgf", argv[0]);

	char s[QR_CODE_MAX_SIZE+1];
	size_t ret = fread(s, 1, QR_CODE_MAX_SIZE, stdin);
	s[ret] = '\0';

	if ( strlen(s) == 0 )
		die("no data");

	QRcode *qr = QRcode_encodeString8bit(s, 0, QR_ECLEVEL_Q);

	encode_borders(qr);
	print_regions(qr, plug);

	exit(EXIT_SUCCESS);
}

